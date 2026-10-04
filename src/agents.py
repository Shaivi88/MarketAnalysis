import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool

load_dotenv()

os.environ["SERPAPI_API_KEY"] = os.getenv("SEARCH_API_KEY", "")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
)

_search = SerpAPIWrapper()
search_tool = Tool(
    name="web_search",
    func=_search.run,
    description=(
        "Search the web for current information about industries, companies, "
        "market trends, pricing updates, and product launches."
    ),
)

scout_agent = Agent(
    role="Market Scout",
    goal=(
        "Monitor the {industry} industry for new market entrants, "
        "pricing updates, and recent product launches."
    ),
    backstory=(
        "You are an expert market researcher specialising in competitive intelligence. "
        "You track industry movements with precision, gathering comprehensive data on "
        "market dynamics, emerging players, and strategic pricing shifts."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
)

synthesis_agent = Agent(
    role="Intelligence Synthesizer",
    goal=(
        "Consolidate raw market research into a structured comparative feature matrix "
        "for the {industry} industry."
    ),
    backstory=(
        "You are a senior business analyst skilled at transforming unstructured web findings "
        "into clear, actionable intelligence. You excel at spotting patterns and building "
        "side-by-side comparisons that highlight market gaps and opportunities."
    ),
    llm=llm,
    verbose=True,
)

strategy_agent = Agent(
    role="Strategy Consultant",
    goal=(
        "Formulate an executive SWOT analysis and actionable go-to-market recommendations "
        "for the {industry} industry."
    ),
    backstory=(
        "You are a seasoned strategy consultant with deep expertise in corporate strategy "
        "and go-to-market planning. You translate market intelligence into clear strategic "
        "directives that leadership can act on immediately."
    ),
    llm=llm,
    verbose=True,
)
