from crewai import Crew, Process
from src.agents import scout_agent, synthesis_agent, strategy_agent, fetch_search_results
from src.tasks import create_tasks


def run_crew(industry: str) -> dict:
    search_results = fetch_search_results(industry)
    scout_task, synthesis_task, swot_task, brief_task = create_tasks()

    crew = Crew(
        agents=[scout_agent, synthesis_agent, strategy_agent],
        tasks=[scout_task, synthesis_task, swot_task, brief_task],
        process=Process.sequential,
        verbose=True,
    )

    crew.kickoff(inputs={"industry": industry, "search_results": search_results})

    return {
        "swot": swot_task.output.raw,
        "brief": brief_task.output.raw,
    }
