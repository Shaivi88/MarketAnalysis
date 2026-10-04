from crewai import Task
from src.agents import scout_agent, synthesis_agent, strategy_agent


def create_tasks():
    scout_task = Task(
        description=(
            "Search the web comprehensively for the {industry} industry. Identify and document:\n"
            "- New market entrants (companies that entered in the last 1-2 years)\n"
            "- Pricing strategies and recent pricing updates from key players\n"
            "- Recent product launches and notable feature releases\n"
            "- Market size estimates, growth rate, and key statistics\n"
            "- Major incumbent players and their current positioning\n\n"
            "Compile all findings into detailed, structured notes."
        ),
        expected_output=(
            "A detailed research report covering new entrants, pricing data, product launches, "
            "incumbent analysis, and market statistics for the {industry} industry."
        ),
        agent=scout_agent,
    )

    synthesis_task = Task(
        description=(
            "Using the market research provided, produce:\n"
            "1. A comparative feature matrix as a markdown table comparing incumbents vs "
            "new entrants across key dimensions (pricing, core features, target market, "
            "key differentiators, funding/scale).\n"
            "2. A concise summary of the top 3-5 market trends observed.\n"
            "3. A list of market gaps and opportunities identified."
        ),
        expected_output=(
            "A structured synthesis containing a markdown comparison table, key market trends, "
            "and identified opportunities for the {industry} industry."
        ),
        agent=synthesis_agent,
        context=[scout_task],
    )

    swot_task = Task(
        description=(
            "Based on the market synthesis, write a comprehensive executive SWOT analysis "
            "for a leadership team evaluating the {industry} industry.\n\n"
            "Format as a complete markdown document with:\n"
            "- A title (e.g. '# SWOT Analysis: {industry} Industry')\n"
            "- A short executive summary paragraph\n"
            "- Four clearly labelled sections: ## Strengths, ## Weaknesses, "
            "## Opportunities, ## Threats\n"
            "- 4-6 bullet points per section, each with a one-sentence explanation\n"
            "- A concluding ## Strategic Outlook paragraph"
        ),
        expected_output=(
            "A complete, well-structured SWOT analysis markdown document for the {industry} industry."
        ),
        agent=strategy_agent,
        context=[synthesis_task],
        output_file="outputs/swot.md",
    )

    brief_task = Task(
        description=(
            "Based on the market synthesis, write a concise actionable go-to-market brief "
            "for leadership targeting the {industry} industry.\n\n"
            "Format as a complete markdown document with:\n"
            "- A title (e.g. '# Actionable Market Brief: {industry} Industry')\n"
            "- A short executive summary paragraph\n"
            "- ## Strategic Recommendations: top 3-5 recommendations with rationale\n"
            "- ## Key Risks to Monitor: 3-4 risks with brief explanations\n"
            "- ## Immediate Next Steps: suggested 30 / 60 / 90-day actions"
        ),
        expected_output=(
            "A complete, well-structured actionable go-to-market brief markdown document "
            "for the {industry} industry."
        ),
        agent=strategy_agent,
        context=[synthesis_task],
        output_file="outputs/actionable_brief.md",
    )

    return scout_task, synthesis_task, swot_task, brief_task
