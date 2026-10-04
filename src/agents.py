import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import tool
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

os.environ["SERPAPI_API_KEY"] = os.getenv("SEARCH_API_KEY", "")
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY", "")

_search = SerpAPIWrapper()

@tool("web_search")
def search_tool(query: str) -> str:
    """Search the web for current information about industries, companies, market trends, pricing updates, and product launches."""
    return _search.run(query)

_llm = "openai/gpt-oss-20b"

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
    llm=_llm,
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
    llm=_llm,
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
    llm=_llm,
    verbose=True,
)
