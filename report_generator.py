import re
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from models import Report, Research
import streamlit as st
# import os
# from dotenv import load_dotenv
from tools import general_and_finance_search, news_search

# load_dotenv()

# NVIDIA_API = os.getenv("NVIDIA_API")

tools = [general_and_finance_search, news_search]

# client = ChatNVIDIA(
#     model="deepseek-ai/deepseek-r1",
#     api_key=NVIDIA_API,
#     temperature=0,
#     max_tokens=4096,
# )

client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)
llm_with_tools = client.bind_tools(tools=tools)

def report_str_llm(state: Report):
    contents = f"""You are an expert in designing detailed structures and outlines for content. Your task is to generate a well-organized and comprehensive content outline.
Each section of the outline should include a brief description, key points, and references (except intro and conclusion sections).
Please use the following parameters:
- Topic: {state['topic']}
- Content Type: {state['report_type']}
- Overall Outline: {state['outline']}
Generate a structured content outline that adheres to these guidelines.
Make sure to only provide a structure for the content.
Think very deeply as an expert content writer to structure and enhance the content's appeal.
"""
prompt = ChatPromptTemplate.from_template("{contents}")
chain = prompt | llm_with_tools | StrOutputParser()
response = chain.invoke({"contents": contents})
    cleaned_response = re.sub(r"<think>.*?</think>\n?", "", response, flags=re.DOTALL)
    state["report_structure"] = cleaned_response
    state["messages"] = prompt.format_prompt(**{
        "topic": state["topic"],
        "report_type": state["report_type"],
        "outline": state["outline"],
    }).to_messages()
    return state

def researcher(state: Research):
    messages = [
        (
            "system",
            """You are an expert researcher tasked with performing deep and extensive research on the given topic.
Your output should have two parts:
1. **Queries**: Generate a list of search queries (each on a separate line or numbered) that are relevant to the topic and overall outline.
2. **Deep Research**: For each generated query, provide detailed research findings including recent advancements, news articles, academic sources, and relevant data. If you need to fetch up‑to‑date information, include a tool command in the following format:
    <tool: news_search | query: "your search query here">
Include references with URL links in markdown format.
Here are the input values:
  - **Topic**: {topic}
  - **Overall Outline**: {outline}
Your output should be structured with a clear separation between the Queries and the Deep Research sections.
"""
        ),
    ]
    prompt = ChatPromptTemplate(messages)
    chain = prompt | llm_with_tools | StrOutputParser()
    response = chain.invoke({
        "topic": state["topic"],
        "outline": state["outline"],
    })
    cleaned_response = re.sub(r"<think>.*?</think>\n?", "", response, flags=re.DOTALL)

    # Parse the output: assume the model returns text with "Queries:" and "Deep Research:" sections.
    # Example expected output:
    #   Queries:
    #   1. query one
    #   2. query two
    #
    #   Deep Research:
    #   Detailed findings for query one...
    #   Detailed findings for query two...
    parts = cleaned_response.split("Deep Research:")
    if len(parts) == 2:
        queries_section = parts[0].split("Queries:")[-1].strip()
        research_section = parts[1].strip()
    else:
        queries_section = ""
        research_section = cleaned_response

    # Process queries: split by newline and clean up
    queries_list = [line.strip("- ").strip() for line in queries_section.split("\n") if line.strip()]
    # If the queries are comma separated, split them as well.
    if not queries_list and queries_section:
        queries_list = [q.strip() for q in queries_section.split(",") if q.strip()]

    state["queries"].extend(queries_list)
    state["deep_research"].append(research_section)
    state["messages"] = prompt.format_prompt(**{
        "topic": state["topic"],
        "outline": state["outline"],
    }).to_messages()
    return state

def report_content(state: Report):
    messages = [
        (
            "system",
            """You are an expert content writer. Your task is to generate and curate a well-organized, comprehensive content piece.
Each section of the outline should be detailed and easy to understand, following the provided structure.
Please use the following parameters:
- **Topic**: {topic}
- **Content Type**: {report_type}
- **Overall Outline**: {outline}
- **Report Structure**: {report_structure}
Generate content that adheres to these guidelines.
Ensure that each section is at least 200 words for the introduction and conclusion, at least 500 words for other sections, and that each subsection has at least 200 words.
Include reference URL links in markdown format.
Provide the entire content in markdown format enclosed between <report> and </report>.
Provide a desirable title for the content.
The content should be structured in pandoc markdown format to convert the markdown to a pdf
"""
        ),
    ]
    prompt = ChatPromptTemplate(messages)
    chain = prompt | llm_with_tools | StrOutputParser()
    response = chain.invoke({
        "topic": state["topic"],
        "report_type": state["report_type"],
        "outline": state["outline"],
        "report_structure": state["report_structure"]
    })
    cleaned_response = re.sub(r"<think>.*?</think>\n?", "", response, flags=re.DOTALL)
    state["final_report"] = cleaned_response
    state["messages"] = prompt.format_prompt(**{
        "topic": state["topic"],
        "report_type": state["report_type"],
        "outline": state["outline"],
        "report_structure": state["report_structure"]
    }).to_messages()
    return state
