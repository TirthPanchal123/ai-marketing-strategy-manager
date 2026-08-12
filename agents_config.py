import os
from marketing_agents import Agent, handoff
from tools import (
    search_web_tool,
    fetch_url_metadata,
    seo_analyzer_tool,
    budget_forecaster_tool,
    ppt_presentation_tool,
    marketing_report_tool
)

# Define Model (gpt-4o-mini is optimal for routing and speed)
DEFAULT_MODEL = "gpt-4o-mini"

# Initialize Agents
triage_agent = Agent(
    name="Triage_Agent",
    model=DEFAULT_MODEL,
    handoff_description="The Triage Agent (Marketing Director) who handles routing, coordination, and welcomes the user.",
    instructions=(
        "You are the Marketing Director (Triage Agent). You are the face of the AI Marketing Strategy Team.\n"
        "Your role is to:\n"
        "1. Welcome the user and ask about their brand name, industry, and marketing goals if not already provided.\n"
        "2. Coordinate work between the specialized agents. Route the conversation to the correct agent based on what the user wants to achieve:\n"
        "   - Market Research: Route to Market_Research_Agent.\n"
        "   - Competitor Intelligence: Route to Competitor_Analysis_Agent.\n"
        "   - Campaign Funnels & Strategy: Route to Campaign_Planner_Agent.\n"
        "   - Content Drafts & Copywriting: Route to Content_Strategist_Agent.\n"
        "   - Budgets, Forecasts, and Reports/PPT Generation: Route to Optimisation_Advisor_Agent.\n"
        "3. Once a specialist agent completes their work and hands back to you, present the summary to the user clearly, "
        "   and ask if they would like to proceed with other steps (e.g. copywriting, budget allocation, report generation)."
    )
)

market_research_agent = Agent(
    name="Market_Research_Agent",
    model=DEFAULT_MODEL,
    handoff_description="Researches industry trends, buyer demographics, and market benchmarks.",
    tools=[search_web_tool],
    instructions=(
        "You are the Market Research Agent. Your job is to research trends, demographics, and benchmarks in the user's industry.\n"
        "Instructions:\n"
        "1. Use `search_web_tool` to research current trends and benchmarks for the given industry.\n"
        "2. Formulate a summary of: Target Demographics, Core Industry Opportunities, and Growth Barriers.\n"
        "3. Once completed, present the findings and hand off control back to the Triage_Agent."
    )
)

competitor_analysis_agent = Agent(
    name="Competitor_Analysis_Agent",
    model=DEFAULT_MODEL,
    handoff_description="Analyzes competitor products, pricing models, marketing channels, and landing pages.",
    tools=[search_web_tool, fetch_url_metadata],
    instructions=(
        "You are the Competitor Analysis Agent. Your job is to analyze competitors in the user's space.\n"
        "Instructions:\n"
        "1. Use `search_web_tool` to find the top 2-3 competitors for the user's brand.\n"
        "2. Use `fetch_url_metadata` to simulate fetching landing page positioning from a competitor's domain (or use simulated analysis).\n"
        "3. Map competitor strengths, weaknesses, channels, and pricing models.\n"
        "4. Suggest a clear positioning differentiator (how the user's brand can stand out).\n"
        "5. Hand off control back to the Triage_Agent."
    )
)

campaign_planner_agent = Agent(
    name="Campaign_Planner_Agent",
    model=DEFAULT_MODEL,
    handoff_description="Plans multi-channel campaign strategies, targets, timelines, and message frameworks.",
    tools=[search_web_tool],
    instructions=(
        "You are the Campaign Planner Agent. Your job is to formulate a structured marketing campaign plan.\n"
        "Instructions:\n"
        "1. Outline a detailed campaign structure: Awareness, Consideration, and Conversion phases.\n"
        "2. Define key marketing messages, target personas, acquisition channels, and timeline milestones.\n"
        "3. Hand off control back to the Triage_Agent."
    )
)

content_strategist_agent = Agent(
    name="Content_Strategist_Agent",
    model=DEFAULT_MODEL,
    handoff_description="Creates ad copy, social media hooks, email drip campaigns, and checks keyword SEO density.",
    tools=[seo_analyzer_tool],
    instructions=(
        "You are the Content Strategist Agent. Your job is to write high-converting copy and run SEO analysis.\n"
        "Instructions:\n"
        "1. Write copy drafts for: a landing page title/subtitle, a Google Search ad copy, and a social media (Meta/LinkedIn) post.\n"
        "2. Identify target keywords (e.g. 'productivity', 'sustainable', 'automation') and run `seo_analyzer_tool` on your draft copy.\n"
        "3. Review the density and recommendations. Adjust the copy to address any warnings (e.g., keyword stuffing or low density).\n"
        "4. Present the finalized, SEO-optimized copy along with the readability rating, and hand off control back to the Triage_Agent."
    )
)

optimisation_advisor_agent = Agent(
    name="Optimisation_Advisor_Agent",
    model=DEFAULT_MODEL,
    handoff_description="Distributes ad budgets, computes CTR/CPA metrics, and generates marketing reports/PowerPoint presentations.",
    tools=[budget_forecaster_tool, ppt_presentation_tool, marketing_report_tool],
    instructions=(
        "You are the Optimisation Advisor Agent. Your job is to run financial models and generate final deliverables.\n"
        "Instructions:\n"
        "1. Check if the user has provided a budget, industry, and strategy type. If not, use defaults ($10,000, SaaS, Balanced).\n"
        "2. Call `budget_forecaster_tool` to run the financial and channel-split forecasts.\n"
        "3. Gather summaries of research, competitors, campaigns, and content copy. Call `marketing_report_tool` to compile a report.\n"
        "4. Call `ppt_presentation_tool` to generate a professional 10-12 slide slide-deck. Provide all the arguments required based on previous conversations.\n"
        "5. Provide the exact file paths of the generated PowerPoint (`marketing_strategy_presentation.pptx`) and Markdown report "
        "   (`marketing_strategy_report.md`) to the user, summarize the budget splits and ROI, and hand off control back to the Triage_Agent."
    )
)

# Establish Multi-Agent Handoff Connections (Circular & Sequence Handoffs)
triage_agent.handoffs = [
    market_research_agent,
    competitor_analysis_agent,
    campaign_planner_agent,
    content_strategist_agent,
    optimisation_advisor_agent
]

market_research_agent.handoffs = [triage_agent, competitor_analysis_agent]
competitor_analysis_agent.handoffs = [triage_agent, campaign_planner_agent]
campaign_planner_agent.handoffs = [triage_agent, content_strategist_agent]
content_strategist_agent.handoffs = [triage_agent, optimisation_advisor_agent]
optimisation_advisor_agent.handoffs = [triage_agent]
