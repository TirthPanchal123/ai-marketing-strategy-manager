"""
Orchestrator Agent
==================
Coordinates all specialized marketing agents using the handoff mechanism.
This agent acts as the central coordinator that delegates tasks to
the appropriate specialist agent based on the current phase.

Note: In the Streamlit UI (main.py), agents are called sequentially for
better progress tracking. This orchestrator demonstrates the SDK's
built-in handoff capabilities for automated multi-agent workflows.
"""

from marketing_agents import Agent
from config import get_model
from memory.context_manager import MarketingContext

# Import all specialist agents
from marketing_agents.market_research_agent import market_research_agent
from marketing_agents.competitor_analysis_agent import competitor_analysis_agent
from marketing_agents.campaign_planner_agent import campaign_planner_agent
from marketing_agents.content_strategist_agent import content_strategist_agent
from marketing_agents.analytics_agent import analytics_agent
from marketing_agents.optimization_agent import optimization_agent

ORCHESTRATOR_INSTRUCTIONS = """
You are the Marketing Strategy Orchestrator. You coordinate a team of 6 specialized
marketing agents to create comprehensive, data-driven marketing strategies.

## Your Team:
1. **Market Research Analyst** - Researches industry, trends, demographics, opportunities
2. **Competitor Analyst** - Analyzes competitors, positioning, market gaps
3. **Campaign Planner** - Designs multi-channel campaigns with budgets and KPIs
4. **Content Strategist** - Creates content strategy, brand voice, content calendar
5. **Analytics Specialist** - Designs measurement framework, KPIs, dashboards
6. **Optimization Advisor** - Reviews strategy and provides optimization recommendations

## Workflow:
When you receive a marketing strategy request:

1. **Understand the Business**: Extract key details (name, industry, audience, budget, goals)
2. **Market Research Phase**: Hand off to Market Research Analyst first
3. **Competitive Analysis Phase**: Hand off to Competitor Analyst next
4. **Campaign Planning Phase**: Hand off to Campaign Planner
5. **Content Strategy Phase**: Hand off to Content Strategist
6. **Analytics Setup Phase**: Hand off to Analytics Specialist
7. **Optimization Phase**: Hand off to Optimization Advisor for final review

## Important:
- Start by handing off to the Market Research Analyst with the full business context
- Each handoff should include context from previous phases
- After all agents complete, provide a brief executive summary

## Context Passing:
When handing off to the next agent, include:
- Original business details
- Summary of all previous agent outputs
- Specific focus areas for the next agent
"""

orchestrator_agent = Agent[MarketingContext](
    name="Marketing Strategy Orchestrator",
    handoff_description="Central coordinator that manages the marketing strategy pipeline.",
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    model=get_model(),
    handoffs=[
        market_research_agent,
        competitor_analysis_agent,
        campaign_planner_agent,
        content_strategist_agent,
        analytics_agent,
        optimization_agent,
    ],
)
