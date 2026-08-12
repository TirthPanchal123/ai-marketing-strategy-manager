"""
Pydantic schemas for structured outputs from each marketing agent.
These models define the expected output format for each specialized agent.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ─── Market Research Agent Output ─────────────────────────────────────────

class MarketTrend(BaseModel):
    """A single market trend identified during research."""
    trend_name: str = Field(description="Name of the market trend")
    description: str = Field(description="Detailed description of the trend")
    relevance_score: float = Field(description="Relevance score from 0 to 10")
    source: str = Field(default="", description="Source of the trend data")


class MarketResearchOutput(BaseModel):
    """Structured output from the Market Research Agent."""
    industry_overview: str = Field(description="Overview of the industry landscape")
    market_size: str = Field(description="Estimated market size and growth")
    target_demographics: List[str] = Field(description="Key target demographic segments")
    trends: List[MarketTrend] = Field(description="Current market trends")
    opportunities: List[str] = Field(description="Key market opportunities")
    threats: List[str] = Field(description="Potential market threats")
    key_insights: List[str] = Field(description="Top actionable insights")


# ─── Competitor Analysis Agent Output ─────────────────────────────────────

class Competitor(BaseModel):
    """Analysis of a single competitor."""
    name: str = Field(description="Competitor name")
    strengths: List[str] = Field(description="Key strengths")
    weaknesses: List[str] = Field(description="Key weaknesses")
    market_position: str = Field(description="Market positioning")
    digital_presence: str = Field(description="Digital presence assessment")
    unique_selling_point: str = Field(description="Their USP")


class CompetitorAnalysisOutput(BaseModel):
    """Structured output from the Competitor Analysis Agent."""
    competitors: List[Competitor] = Field(description="Analyzed competitors")
    market_gaps: List[str] = Field(description="Identified market gaps")
    competitive_advantages: List[str] = Field(description="Our competitive advantages")
    positioning_recommendation: str = Field(description="Recommended market positioning")


# ─── Campaign Planner Agent Output ────────────────────────────────────────

class CampaignIdea(BaseModel):
    """A single marketing campaign idea."""
    name: str = Field(description="Campaign name")
    objective: str = Field(description="Campaign objective")
    target_audience: str = Field(description="Target audience for this campaign")
    channels: List[str] = Field(description="Marketing channels to use")
    budget_allocation: str = Field(description="Suggested budget allocation")
    timeline: str = Field(description="Campaign timeline")
    kpis: List[str] = Field(description="Key performance indicators")
    description: str = Field(description="Detailed campaign description")


class CampaignPlanOutput(BaseModel):
    """Structured output from the Campaign Planner Agent."""
    campaign_theme: str = Field(description="Overall campaign theme")
    campaigns: List[CampaignIdea] = Field(description="Individual campaign ideas")
    total_budget_recommendation: str = Field(description="Total budget recommendation")
    priority_order: List[str] = Field(description="Priority order for campaigns")


# ─── Content Strategist Agent Output ──────────────────────────────────────

class ContentPiece(BaseModel):
    """A single content piece in the content calendar."""
    content_type: str = Field(description="Type: blog, social, email, video, infographic")
    title: str = Field(description="Content title/headline")
    description: str = Field(description="Content description")
    platform: str = Field(description="Target platform")
    tone: str = Field(description="Tone of voice")
    call_to_action: str = Field(description="Call to action")
    sample_copy: str = Field(description="Sample copy/draft")


class ContentStrategyOutput(BaseModel):
    """Structured output from the Content Strategist Agent."""
    brand_voice: str = Field(description="Recommended brand voice")
    content_pillars: List[str] = Field(description="Content pillar topics")
    content_calendar: List[ContentPiece] = Field(description="Content pieces")
    distribution_strategy: str = Field(description="Content distribution strategy")
    engagement_tactics: List[str] = Field(description="Engagement tactics")


# ─── Analytics Agent Output ───────────────────────────────────────────────

class MetricRecommendation(BaseModel):
    """A recommended KPI or metric to track."""
    metric_name: str = Field(description="Name of the metric")
    description: str = Field(description="What this metric measures")
    target_value: str = Field(description="Recommended target value")
    measurement_tool: str = Field(description="Tool to measure this metric")


class AnalyticsOutput(BaseModel):
    """Structured output from the Analytics Agent."""
    recommended_kpis: List[MetricRecommendation] = Field(description="Recommended KPIs")
    tracking_setup: List[str] = Field(description="Tracking setup recommendations")
    reporting_frequency: str = Field(description="How often to report")
    dashboard_components: List[str] = Field(description="Dashboard components")
    attribution_model: str = Field(description="Recommended attribution model")


# ─── Optimization Advisor Agent Output ────────────────────────────────────

class OptimizationSuggestion(BaseModel):
    """A single optimization suggestion."""
    area: str = Field(description="Area of optimization")
    current_state: str = Field(description="Current state assessment")
    recommendation: str = Field(description="Optimization recommendation")
    expected_impact: str = Field(description="Expected impact")
    priority: str = Field(description="Priority: High/Medium/Low")


class OptimizationOutput(BaseModel):
    """Structured output from the Optimization Advisor Agent."""
    quick_wins: List[OptimizationSuggestion] = Field(description="Quick wins")
    long_term_improvements: List[OptimizationSuggestion] = Field(description="Long-term")
    ab_test_ideas: List[str] = Field(description="A/B testing ideas")
    budget_optimization: str = Field(description="Budget optimization tips")
    overall_score: float = Field(description="Marketing readiness score 0-100")
