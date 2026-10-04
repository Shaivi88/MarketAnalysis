import os
from crewai import Crew, Process
from src.agents import scout_agent, synthesis_agent, strategy_agent
from src.tasks import create_tasks

os.makedirs("outputs", exist_ok=True)


def run_crew(industry: str) -> dict:
    scout_task, synthesis_task, swot_task, brief_task = create_tasks()

    crew = Crew(
        agents=[scout_agent, synthesis_agent, strategy_agent],
        tasks=[scout_task, synthesis_task, swot_task, brief_task],
        process=Process.sequential,
        verbose=True,
    )

    crew.kickoff(inputs={"industry": industry})

    return {
        "swot": "outputs/swot.md",
        "brief": "outputs/actionable_brief.md",
    }
