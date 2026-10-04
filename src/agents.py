import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai.tools import tool
from serpapi import GoogleSearch

load_dotenv()

@tool("web_search")
def search_tool(query: str) -> str:
    """Search the web for current information about industries, companies, market trends, pricing updates, and product launches."""
    results = GoogleSearch({"q": query, "api_key": os.getenv("SEARCH_API_KEY", ""), "num": 8}).get_dict()
    organic = results.get("organic_results", [])
    return "\n".join(f"{r.get('title', '')}: {r.get('snippet', '')}" for r in organic)

_llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
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
