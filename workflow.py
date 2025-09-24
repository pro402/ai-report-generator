from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from models import Report, Research
from report_generator import report_str_llm, report_content, researcher
from tools import general_and_finance_search, news_search

tools = [general_and_finance_search, news_search]

# ---- Research Graph Definition ----
research_graph = StateGraph(Research)
research_graph.add_node("researcher", researcher)
research_graph.add_node("research_tools", ToolNode(tools))
research_graph.add_edge(START, "researcher")
research_graph.add_conditional_edges(
    "researcher",
    tools_condition,
    {"tool": "research_tools", "default": END}  # <--- Only use END here
)
research_graph.add_edge("research_tools", "researcher")
graphh = research_graph.compile()

# ---- Main Workflow Definition ----
workflow = StateGraph(Report)
workflow.add_node("generate_report_structure", report_str_llm)
workflow.add_node("structure_tools", ToolNode(tools))
workflow.add_node("report_content_generator", report_content)
workflow.add_node("researcher", graphh)

workflow.add_edge(START, "generate_report_structure")
workflow.add_conditional_edges(
    "generate_report_structure",
    tools_condition,
    {"tool": "structure_tools", "default": "researcher"}  # <--- Valid nodes only
)
workflow.add_edge("structure_tools", "generate_report_structure")
workflow.add_edge("researcher", "report_content_generator")
workflow.add_edge("report_content_generator", END)  # <--- Use END, not "__end__"

graph = workflow.compile()
