# File: src/codelibre/graph/graph.py
from langgraph.graph import StateGraph, END 
from codelibre.graph.state import ChatState
from codelibre.graph.nodes import truncate_messages, ask, add_input, update_conversation_history


def build_chat_graph():
    graph = StateGraph(ChatState)

    # Add nodes
    graph.add_node("truncate_messages", truncate_messages)
    graph.add_node("ask", ask)
    graph.add_node("update_conversation_history", update_conversation_history)
    graph.add_node("add_input", add_input)

    # Wire it up
    graph.set_entry_point("truncate_messages")
    graph.add_edge("truncate_messages", "ask")
    graph.add_edge("ask", "update_conversation_history")
    graph.add_edge("update_conversation_history", "add_input")
    graph.add_conditional_edges(
        "add_input",
        lambda state: END if not state.reiterate else "truncate_messages"
    )

    return graph
