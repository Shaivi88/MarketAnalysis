import os
import litellm
from dotenv import load_dotenv
from crewai import Agent, LLM
from serpapi import GoogleSearch

load_dotenv()

litellm.num_retries = 6
litellm.retry_after = 10


def fetch_search_results(industry: str) -> str:
    queries = [
        f"{industry} market new entrants 2024 2025",
        f"{industry} market size growth rate statistics 2024",
    ]
    lines = []
    api_key = os.getenv("SEARCH_API_KEY", "")
    for q in queries:
        results = GoogleSearch({"q": q, "api_key": api_key, "num": 3}).get_dict()
        organic = results.get("organic_results", [])
        for r in organic:
            snippet = r.get("snippet", "")[:200]
            lines.append(f"{r.get('title', '')}: {snippet}")
    return "\n".join(lines)


_llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)

scout_agent = Agent(
    role="Market Scout",
    goal=(
        "Analyse pre-fetched web research on the {industry} industry and identify "
        "new market entrants, pricing updates, and recent product launches."
    ),
    backstory=(
        "You are an expert market researcher specialising in competitive intelligence. "
        "You track industry movements with precision, gathering comprehensive data on "
        "market dynamics, emerging players, and strategic pricing shifts."
    ),
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
