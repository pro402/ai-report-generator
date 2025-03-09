from langchain_core.tools import tool
from typing_extensions import Literal
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@tool
def general_and_finance_search(
    query: str,
    search_topic: Literal["general", "finance"] = "general",
    search_depth: Literal["advanced", "basic"] = "advanced",
    max_results: int = 5,
    time_range: Literal["none", "day", "week", "month", "year"] = "none",
    include_answer: Literal["advanced", "basic", "none"] = "advanced",
):
    """
    This function will return the general and finance search results for the given query.
    Args:
        query: str, The query to run a search on.
        search_topic: The topic of the search.
        search_depth: The depth of the search. It can be "basic" or "advanced".
        max_results: The maximum number of search results to return. It must be between 0 and 20.
        time_range: The time range back from the current date.
        include_answer = Literal["advanced", "basic", "none"] = "advanced"
    Returns:
        response: dict
    """
    client = TavilyClient(TAVILY_API_KEY)
    response = client.search(
        query=query,
        topic=search_topic,
        search_depth=search_depth,
        max_results=max_results,
        time_range=time_range,
        include_answer=include_answer,
        include_images=True,
        include_image_descriptions=True,
        include_raw_content=True,
    )
    # print(response)
    return response

@tool
def news_search(
    query: str,
    search_depth: Literal["advanced", "basic"] = "advanced",
    max_results: int = 5,
    time_range: Literal["none", "day", "week", "month", "year"] = "none",
    include_answer: Literal["advanced", "basic", "none"] = "advanced",
    days: int = 3
):
    """
    This function will return the news search results for the given query.
    Args:
        query: str, The query to run a search on.
        search_depth: The depth of the search. It can be "basic" or "advanced".
        max_results: The maximum number of search results to return. It must be between 0 and 20.
        time_range: The time range back from the current date.
        include_answer = Literal["advanced", "basic", "none"] = "advanced"
        days: The number of days back from the current date to include in the results.
    Returns:
        response: dict
    """
    client = TavilyClient(TAVILY_API_KEY)
    response = client.search(
        query=query,
        topic="news",
        search_depth=search_depth,
        max_results=max_results,
        time_range=time_range,
        include_answer=include_answer,
        include_images=True,
        include_image_descriptions=True,
        include_raw_content=True,
        days=days
    )
    # print(response)
    return response

# @tool
# def human_feedback(
#     feedback: str
# ):
#     """
#     This is a tool that takes feedback from the user on the generated content.
#     """
