from langgraph.graph import StateGraph, END
from langgraph_chat.state import ChatState
from langgraph_chat.nodes import process_query

def build_stateless_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("process_query", process_query)
    graph.set_entry_point("process_query")
    graph.add_edge("process_query", END)
    return graph.compile()

def create_stateless_chat():
    return build_stateless_chat_graph()
