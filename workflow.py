from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_input: str
    route: str


def classify_request(state: AgentState):
    """Decide which part of the assistant should handle the request."""

    text = state["user_input"].lower()

    calendar_keywords = (
        "calendar",
        "schedule",
        "meeting",
        "appointment",
        "event",
        "موعد",
        "اجتماع",
        "التقويم",
    )

    if any(keyword in text for keyword in calendar_keywords):
        route = "calendar"
    else:
        route = "assistant"

    return {"route": route}


def route_request(state: AgentState) -> Literal["calendar", "assistant"]:
    return state["route"]


def calendar_node(state: AgentState):
    return state


def assistant_node(state: AgentState):
    return state


builder = StateGraph(AgentState)

builder.add_node("classify", classify_request)
builder.add_node("calendar", calendar_node)
builder.add_node("assistant", assistant_node)

builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    route_request,
    {
        "calendar": "calendar",
        "assistant": "assistant",
    },
)

builder.add_edge("calendar", END)
builder.add_edge("assistant", END)

workflow = builder.compile()