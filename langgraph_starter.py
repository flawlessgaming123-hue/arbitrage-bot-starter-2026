"""
LangGraph + Anthropic production agent for arbitrage scanning.

This is the upgrade path from Ralph bash loops to a real state machine.
Use this when you need:
  - Conditional branching (scan -> risk check -> execute OR alert)
  - Parallel tool execution
  - Persistent checkpointing across runs
  - Human-in-the-loop approval gates

Install: pip install -r requirements.txt
Run:     python langgraph_starter.py
"""

import json
import os
from datetime import datetime, timezone
from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# --- State ---

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    scan_results: list[dict]
    risk_decisions: list[dict]
    alerts_sent: int


# --- Tools ---

@tool
def fetch_prices(market: str) -> str:
    """Fetch current prediction market prices.

    Args:
        market: Market name — 'polymarket', 'kalshi', or 'predictit'
    """
    # TODO: Replace with real API calls
    # This stub returns sample data so the graph runs end-to-end
    sample_prices = {
        "polymarket": [
            {"contract": "BTC > 100k by July", "yes_price": 0.6234, "no_price": 0.3766},
            {"contract": "Fed rate cut June", "yes_price": 0.4512, "no_price": 0.5488},
        ],
        "kalshi": [
            {"contract": "BTC > 100k by July", "yes_price": 0.6089, "no_price": 0.3911},
            {"contract": "Fed rate cut June", "yes_price": 0.4701, "no_price": 0.5299},
        ],
    }
    prices = sample_prices.get(market, [])
    return json.dumps({"market": market, "prices": prices, "fetched_at": datetime.now(timezone.utc).isoformat()})


@tool
def calculate_spread(contract: str, price_a: float, price_b: float, fee_pct: float = 0.02) -> str:
    """Calculate net arbitrage spread between two market prices.

    Args:
        contract: Contract name
        price_a: Price on market A
        price_b: Price on market B
        fee_pct: Combined fee estimate (default 2%)
    """
    gross_spread = abs(price_a - price_b)
    net_spread = gross_spread - fee_pct
    return json.dumps({
        "contract": contract,
        "gross_spread": round(gross_spread, 4),
        "net_spread": round(net_spread, 4),
        "profitable": net_spread > 0.005,
    })


@tool
def check_risk(trade_size_usd: float, portfolio_value: float = 10000.0) -> str:
    """Check if a proposed trade passes risk limits.

    Args:
        trade_size_usd: Proposed trade size in USD
        portfolio_value: Total portfolio value (default $10,000)
    """
    pct_of_portfolio = (trade_size_usd / portfolio_value) * 100
    approved = pct_of_portfolio <= 2.0
    return json.dumps({
        "approved": approved,
        "trade_size_usd": trade_size_usd,
        "pct_of_portfolio": round(pct_of_portfolio, 2),
        "reason": "Within 2% limit" if approved else f"Exceeds 2% limit ({pct_of_portfolio:.1f}%)",
    })


@tool
def send_alert(message: str) -> str:
    """Send a Telegram alert for high-edge opportunities.

    Args:
        message: Alert message to send
    """
    # TODO: Wire up to real Telegram bot
    print(f"[ALERT] {message}")
    return json.dumps({"sent": True, "channel": "telegram", "message": message})


# --- Graph ---

def build_graph():
    tools = [fetch_prices, calculate_spread, check_risk, send_alert]

    model = ChatAnthropic(
        model="claude-sonnet-4-6",
        max_tokens=4096,
    ).bind_tools(tools)

    tool_node = ToolNode(tools)

    def agent(state: AgentState):
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# --- Entry point ---

def main():
    app = build_graph()

    print("=" * 60)
    print("Arbitrage Bot — LangGraph Production Agent")
    print("=" * 60)
    print()

    prompt = """You are an arbitrage scanner for prediction markets.

1. Fetch prices from 'polymarket' and 'kalshi'
2. For each matching contract, calculate the spread
3. If any spread is profitable (net > 0.5%), run a risk check for a $100 trade
4. If risk check passes, send an alert with the opportunity details
5. Summarize all findings"""

    result = app.invoke(
        {"messages": [HumanMessage(content=prompt)], "scan_results": [], "risk_decisions": [], "alerts_sent": 0},
        config={"configurable": {"thread_id": f"scan-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"}},
    )

    # Print final response
    final_message = result["messages"][-1]
    print()
    print("--- Agent Response ---")
    print(final_message.content)


if __name__ == "__main__":
    main()
