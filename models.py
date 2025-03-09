from typing import TypedDict, List, Union, Annotated
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing_extensions import Literal
from operator import add

class Report(TypedDict):
    topic: str
    report_type: Literal["Report", "News Letter", "Blog"]
    queries: Annotated[list, add]
    deep_research: Annotated[list, add]
    outline: str
    report_structure: Union[None, str]
    final_report: Union[None, str]
    messages: List[Union[SystemMessage, HumanMessage, AIMessage]]

class Research(TypedDict):
    topic: str
    outline: str
    queries: Annotated[list, add]
    deep_research: Annotated[list, add]
    messages: List[Union[SystemMessage, HumanMessage, AIMessage]]