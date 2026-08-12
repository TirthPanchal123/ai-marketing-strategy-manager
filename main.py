"""
AI Marketing Strategy Manager - Streamlit Web Application
==========================================================
A multi-agent AI platform that generates comprehensive marketing strategies
using specialized AI agents powered by Groq's LLM inference.

Run with: streamlit run main.py
"""

import streamlit as st
import asyncio
import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── Page Configuration ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Marketing Strategy Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #F093FB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.8rem;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    
    .gradient-text-sm {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.4rem;
    }
    
    /* Tagline */
    .tagline {
        color: #8B95A5;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Agent cards */
    .agent-card {
        background: linear-gradient(145deg, #1A1F2E 0%, #252B3B 100%);
        border: 1px solid #2D3548;
        border-radius: 16px;
        padding: 24px;
        margin: 8px 0;
        transition: all 0.3s ease;
        min-height: 160px;
    }
    
    .agent-card:hover {
        border-color: #667EEA;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .agent-card .agent-icon {
        font-size: 2rem;
        margin-bottom: 12px;
    }
    
    .agent-card .agent-title {
        color: #E8ECF1;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 8px;
    }
    
    .agent-card .agent-desc {
        color: #8B95A5;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    
    /* Result container */
    .result-container {
        background: linear-gradient(145deg, #1A1F2E 0%, #1E2435 100%);
        border: 1px solid #2D3548;
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 4px;
    }
    
    .status-pending {
        background: rgba(45, 53, 72, 0.8);
        color: #8B95A5;
    }
    
    .status-running {
        background: rgba(102, 126, 234, 0.2);
        color: #667EEA;
        animation: pulse 2s infinite;
    }
    
    .status-completed {
        background: rgba(0, 212, 170, 0.15);
        color: #00D4AA;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Sidebar styling */
    .sidebar-title {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 4px;
    }
    
    .sidebar-subtitle {
        color: #8B95A5;
        font-size: 0.78rem;
        text-align: center;
        margin-bottom: 16px;
    }
    
    /* Metric cards */
    .metric-card {
        background: #1A1F2E;
        border-left: 4px solid #667EEA;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 8px 0;
    }
    
    .metric-card .metric-label {
        color: #8B95A5;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .metric-value {
        color: #E8ECF1;
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    /* Architecture flow */
    .flow-container {
        background: linear-gradient(145deg, #1A1F2E 0%, #252B3B 100%);
        border: 1px solid #2D3548;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 20px 0;
    }
    
    .flow-arrow {
        color: #667EEA;
        font-size: 1.5rem;
        margin: 0 8px;
    }
    
    .flow-step {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 8px 16px;
        margin: 4px;
        color: #E8ECF1;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Footer */
    .sidebar-footer {
        text-align: center;
        color: #4A5568;
        font-size: 0.72rem;
        padding: 16px 0;
        border-top: 1px solid #2D3548;
        margin-top: 24px;
    }
    
    /* Tab content */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    /* Download button */
    .download-btn {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        color: white;
        font-weight: 600;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ────────────────────────────────────────
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "api_key": "",
        "business_name": "",
        "industry": "",
        "business_description": "",
        "target_audience": "",
        "budget": "",
        "goals": "",
        "website_url": "",
        "competitors": "",
        "market_research_result": None,
        "competitor_analysis_result": None,
        "campaign_plan_result": None,
        "content_strategy_result": None,
        "analytics_result": None,
        "optimization_result": None,
        "strategy_generated": False,
        "generation_phase": "",
        "campaign_approved": False,
        "campaign_rejected": False,
        "generation_time": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ─── Agent Runner ────────────────────────────────────────────────────────
async def run_agent_async(agent, prompt, context):
    """Run an agent asynchronously and return the result."""
    from marketing_agents import Runner

    result = await Runner.run(
        agent,
        input=prompt,
        context=context,
        max_turns=10,
)
    return result.final_output

def run_agent(agent, prompt, context):
    """Synchronous wrapper for running an agent."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(run_agent_async(agent, prompt, context))
    finally:
        loop.close()


# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">🚀 Marketing Strategy</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Powered by Groq + OpenAI Agents SDK</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # API Key
    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="gsk_...",
        help="Get your free API key from console.groq.com"
    )
    if api_key:
        st.session_state.api_key = api_key
        os.environ["GROQ_API_KEY"] = api_key
    
    st.markdown("---")
    
    # Business Details
    with st.expander("📋 Business Details", expanded=True):
        business_name = st.text_input(
            "Business Name *",
            value=st.session_state.business_name,
            placeholder="e.g., TechFlow Solutions"
        )
        
        industry = st.text_input(
            "Industry *",
            value=st.session_state.industry,
            placeholder="e.g., SaaS, E-commerce, Healthcare"
        )
        
        business_description = st.text_area(
            "Business Description *",
            value=st.session_state.business_description,
            placeholder="Brief description of your business, products/services...",
            height=80
        )
        
        target_audience = st.text_input(
            "Target Audience *",
            value=st.session_state.target_audience,
            placeholder="e.g., Small business owners, age 25-45"
        )
        
        budget = st.text_input(
            "Marketing Budget",
            value=st.session_state.budget,
            placeholder="e.g., $10,000/month"
        )
        
        goals = st.text_area(
            "Marketing Goals",
            value=st.session_state.goals,
            placeholder="One goal per line, e.g.:\nIncrease brand awareness\nGenerate 500 leads/month\nImprove social media engagement",
            height=80
        )
        
        website_url = st.text_input(
            "Website URL (optional)",
            value=st.session_state.website_url,
            placeholder="https://www.example.com"
        )
        
        competitors = st.text_area(
            "Known Competitors (optional)",
            value=st.session_state.competitors,
            placeholder="One competitor per line",
            height=60
        )
    
    # Update session state
    st.session_state.business_name = business_name
    st.session_state.industry = industry
    st.session_state.business_description = business_description
    st.session_state.target_audience = target_audience
    st.session_state.budget = budget
    st.session_state.goals = goals
    st.session_state.website_url = website_url
    st.session_state.competitors = competitors
    
    st.markdown("---")
    
    # Generate button
    generate_clicked = st.button(
        "🚀 Generate Marketing Strategy",
        type="primary",
        use_container_width=True,
        disabled=not all([api_key, business_name, industry, business_description, target_audience])
    )
    
    if not all([api_key, business_name, industry, business_description, target_audience]):
        st.caption("⚠️ Fill in all required fields (*) and API key to proceed.")
    
    # Footer
    st.markdown(
        '<div class="sidebar-footer">'
        'Built with ❤️ using OpenAI Agents SDK & Groq<br>'
        'Summer School &#39;26 Capstone Project'
        '</div>',
        unsafe_allow_html=True
    )


# ─── Main Content Area ───────────────────────────────────────────────────

if generate_clicked and all([api_key, business_name, industry, business_description, target_audience]):
    # ── Strategy Generation ──────────────────────────────────────────
    
    # Update config with API key
    from config import update_api_key
    update_api_key(api_key)
    
    # Import agents (after config is set)
    from marketing_agents.market_research_agent import market_research_agent
    from marketing_agents.competitor_analysis_agent import competitor_analysis_agent
    from marketing_agents.campaign_planner_agent import campaign_planner_agent
    from marketing_agents.content_strategist_agent import content_strategist_agent
    from marketing_agents.analytics_agent import analytics_agent
    from marketing_agents.optimization_agent import optimization_agent
    from memory.context_manager import MarketingContext
    
    # Build context
    goals_list = [g.strip() for g in goals.split("\\n") if g.strip()] if goals else []
    context = MarketingContext(
        business_name=business_name,
        industry=industry,
        business_description=business_description,
        target_audience=target_audience,
        budget=budget if budget else "Not specified",
        goals=goals_list,
        website_url=website_url,
        competitors_input=competitors,
    )
    
    # Build base prompt
    base_context = f"""## Business Information
- **Business Name**: {business_name}
- **Industry**: {industry}
- **Description**: {business_description}
- **Target Audience**: {target_audience}
- **Marketing Budget**: {budget if budget else 'Not specified'}
- **Goals**: {', '.join(goals_list) if goals_list else 'Not specified'}
- **Website**: {website_url if website_url else 'Not provided'}
- **Known Competitors**: {competitors if competitors else 'Not specified'}"""
    
    start_time = time.time()
    
    st.markdown('<p class="gradient-text">🚀 Generating Your Marketing Strategy</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Our AI agents are working together to craft your strategy...</p>', unsafe_allow_html=True)
    
    # Agent pipeline
    agents_pipeline = [
        {
            "name": "📊 Market Research Analyst",
            "agent": market_research_agent,
            "key": "market_research_result",
            "prompt": f"Conduct comprehensive market research for this business:\\n\\n{base_context}",
        },
        {
            "name": "🏢 Competitor Analyst",
            "agent": competitor_analysis_agent,
            "key": "competitor_analysis_result",
            "prompt": None,  # Built dynamically
        },
        {
            "name": "📋 Campaign Planner",
            "agent": campaign_planner_agent,
            "key": "campaign_plan_result",
            "prompt": None,
        },
        {
            "name": "✍️ Content Strategist",
            "agent": content_strategist_agent,
            "key": "content_strategy_result",
            "prompt": None,
        },
        {
            "name": "📈 Analytics Specialist",
            "agent": analytics_agent,
            "key": "analytics_result",
            "prompt": None,
        },
        {
            "name": "⚡ Optimization Advisor",
            "agent": optimization_agent,
            "key": "optimization_result",
            "prompt": None,
        },
    ]
    
    # Run each agent sequentially with progress display
    for i, agent_info in enumerate(agents_pipeline):
        with st.status(f"{agent_info['name']} is analyzing...", expanded=True) as status:
            try:
                # Build prompt with context from previous agents
                if agent_info["prompt"]:
                    prompt = agent_info["prompt"]
                else:
                    prompt = f"{base_context}\\n\\n"
                    
                    # Add previous results as context
                    if st.session_state.market_research_result:
                        prompt += f"## Previous: Market Research Findings\\n{st.session_state.market_research_result[:2000]}\\n\\n"
                    if st.session_state.competitor_analysis_result:
                        prompt += f"## Previous: Competitor Analysis\\n{st.session_state.competitor_analysis_result[:2000]}\\n\\n"
                    if st.session_state.campaign_plan_result:
                        prompt += f"## Previous: Campaign Plan\\n{st.session_state.campaign_plan_result[:2000]}\\n\\n"
                    if st.session_state.content_strategy_result:
                        prompt += f"## Previous: Content Strategy\\n{st.session_state.content_strategy_result[:2000]}\\n\\n"
                    if st.session_state.analytics_result:
                        prompt += f"## Previous: Analytics Framework\\n{st.session_state.analytics_result[:2000]}\\n\\n"
                    
                    prompt += f"Now provide your specialized analysis for {business_name} in the {industry} industry."
                
                # Run the agent
                result = run_agent(agent_info["agent"], prompt, context)
                st.session_state[agent_info["key"]] = result
                
                # Show preview
                st.markdown(result[:500] + "..." if len(result) > 500 else result)
                status.update(label=f"{agent_info['name']} ✅ Complete", state="complete")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                status.update(label=f"{agent_info['name']} ❌ Error", state="error")
                st.session_state[agent_info["key"]] = f"Error occurred: {str(e)}"
    
    # Mark strategy as generated
    elapsed = time.time() - start_time
    st.session_state.strategy_generated = True
    st.session_state.generation_time = round(elapsed, 1)
    st.rerun()


elif st.session_state.strategy_generated:
    # ── Display Results ──────────────────────────────────────────────
    
    st.markdown('<p class="gradient-text">📊 Your Marketing Strategy</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="tagline">Generated for <strong>{st.session_state.business_name}</strong> '
        f'in {st.session_state.generation_time}s</p>',
        unsafe_allow_html=True
    )
    
    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Business", st.session_state.business_name)
    with col2:
        st.metric("🏭 Industry", st.session_state.industry)
    with col3:
        st.metric("⏱️ Gen Time", f"{st.session_state.generation_time}s")
    with col4:
        agents_completed = sum(1 for k in [
            "market_research_result", "competitor_analysis_result",
            "campaign_plan_result", "content_strategy_result",
            "analytics_result", "optimization_result"
        ] if st.session_state.get(k))
        st.metric("🤖 Agents", f"{agents_completed}/6")
    
    st.markdown("---")
    
    # Tabs for results
    tabs = st.tabs([
        "📋 Executive Summary",
        "📊 Market Research",
        "🏢 Competitor Analysis",
        "📋 Campaign Plan",
        "✍️ Content Strategy",
        "📈 Analytics",
        "⚡ Optimization",
    ])
    
    # Executive Summary Tab
    with tabs[0]:
        st.markdown("### 📋 Executive Summary")
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        summary_parts = []
        summary_parts.append(f"# Marketing Strategy for {st.session_state.business_name}")
        summary_parts.append(f"**Industry:** {st.session_state.industry}")
        summary_parts.append(f"**Target Audience:** {st.session_state.target_audience}")
        summary_parts.append(f"**Budget:** {st.session_state.budget or 'Not specified'}")
        summary_parts.append(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        summary_parts.append("")
        summary_parts.append("## Strategy Overview")
        summary_parts.append("This comprehensive marketing strategy was generated by 6 specialized AI agents, each contributing their expertise:")
        summary_parts.append("")
        
        if st.session_state.market_research_result:
            # Extract first paragraph as summary
            mr = st.session_state.market_research_result
            summary_parts.append(f"### 📊 Market Research Highlights")
            summary_parts.append(mr[:600] + "..." if len(mr) > 600 else mr)
            summary_parts.append("")
        
        if st.session_state.optimization_result:
            opt = st.session_state.optimization_result
            summary_parts.append(f"### ⚡ Key Optimization Insights")
            summary_parts.append(opt[:600] + "..." if len(opt) > 600 else opt)
        
        st.markdown("\\n".join(summary_parts))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download full strategy
        full_strategy = f"""{'='*80}
AI MARKETING STRATEGY REPORT
{'='*80}
Business: {st.session_state.business_name}
Industry: {st.session_state.industry}
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
{'='*80}

{'─'*40}
📊 MARKET RESEARCH
{'─'*40}
{st.session_state.market_research_result or 'Not generated'}

{'─'*40}
🏢 COMPETITOR ANALYSIS
{'─'*40}
{st.session_state.competitor_analysis_result or 'Not generated'}

{'─'*40}
📋 CAMPAIGN PLAN
{'─'*40}
{st.session_state.campaign_plan_result or 'Not generated'}

{'─'*40}
✍️ CONTENT STRATEGY
{'─'*40}
{st.session_state.content_strategy_result or 'Not generated'}

{'─'*40}
📈 ANALYTICS FRAMEWORK
{'─'*40}
{st.session_state.analytics_result or 'Not generated'}

{'─'*40}
⚡ OPTIMIZATION RECOMMENDATIONS
{'─'*40}
{st.session_state.optimization_result or 'Not generated'}

{'='*80}
Generated by AI Marketing Strategy Manager
Powered by Groq + OpenAI Agents SDK
{'='*80}
"""
        
        st.download_button(
            label="📥 Download Full Strategy Report",
            data=full_strategy,
            file_name=f"marketing_strategy_{st.session_state.business_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    
    # Market Research Tab
    with tabs[1]:
        st.markdown("### 📊 Market Research Analysis")
        if st.session_state.market_research_result:
            st.markdown(st.session_state.market_research_result)
        else:
            st.info("Market research data not available.")
    
    # Competitor Analysis Tab
    with tabs[2]:
        st.markdown("### 🏢 Competitor Analysis")
        if st.session_state.competitor_analysis_result:
            st.markdown(st.session_state.competitor_analysis_result)
        else:
            st.info("Competitor analysis not available.")
    
    # Campaign Plan Tab
    with tabs[3]:
        st.markdown("### 📋 Campaign Plan")
        if st.session_state.campaign_plan_result:
            st.markdown(st.session_state.campaign_plan_result)
            
            # Human Approval Section
            st.markdown("---")
            st.markdown("### 🤝 Human Approval Required")
            st.markdown("Review the campaign plan above and approve or request changes.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve Campaign Plan", use_container_width=True, type="primary"):
                    st.session_state.campaign_approved = True
                    st.session_state.campaign_rejected = False
                    st.rerun()
            with col2:
                if st.button("❌ Request Changes", use_container_width=True):
                    st.session_state.campaign_rejected = True
                    st.session_state.campaign_approved = False
                    st.rerun()
            
            if st.session_state.campaign_approved:
                st.success("✅ Campaign plan has been APPROVED! Proceeding with implementation.")
            elif st.session_state.campaign_rejected:
                st.warning("⚠️ Campaign plan needs REVISION. Please provide feedback below.")
                feedback = st.text_area("Provide your feedback for revisions:", height=100)
                if feedback and st.button("Submit Feedback"):
                    st.info(f"Feedback noted: {feedback}")
        else:
            st.info("Campaign plan not available.")
    
    # Content Strategy Tab
    with tabs[4]:
        st.markdown("### ✍️ Content Strategy")
        if st.session_state.content_strategy_result:
            st.markdown(st.session_state.content_strategy_result)
        else:
            st.info("Content strategy not available.")
    
    # Analytics Tab
    with tabs[5]:
        st.markdown("### 📈 Analytics Framework")
        if st.session_state.analytics_result:
            st.markdown(st.session_state.analytics_result)
        else:
            st.info("Analytics framework not available.")
    
    # Optimization Tab
    with tabs[6]:
        st.markdown("### ⚡ Optimization Recommendations")
        if st.session_state.optimization_result:
            st.markdown(st.session_state.optimization_result)
        else:
            st.info("Optimization data not available.")
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Generate New Strategy", use_container_width=True):
        for key in [
            "market_research_result", "competitor_analysis_result",
            "campaign_plan_result", "content_strategy_result",
            "analytics_result", "optimization_result",
            "strategy_generated", "campaign_approved", "campaign_rejected",
        ]:
            st.session_state[key] = None if "result" in key else False
        st.rerun()

else:
    # ── Hero Section (Landing Page) ──────────────────────────────────
    
    st.markdown('<p class="gradient-text">AI Marketing Strategy Manager</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Transform your marketing with AI-powered multi-agent intelligence. '
        '6 specialized AI agents work together to create your comprehensive marketing strategy.</p>',
        unsafe_allow_html=True
    )
    
    # Agent cards - Row 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">📊</div>
            <div class="agent-title">Market Research Analyst</div>
            <div class="agent-desc">Analyzes industry trends, market size, demographics, opportunities, and threats using real-time web data.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🏢</div>
            <div class="agent-title">Competitor Analyst</div>
            <div class="agent-desc">Identifies competitors, analyzes their strategies, evaluates SEO performance, and finds market gaps.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">📋</div>
            <div class="agent-title">Campaign Planner</div>
            <div class="agent-desc">Designs multi-channel campaigns with budgets, timelines, KPIs, and creative execution plans.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Agent cards - Row 2
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">✍️</div>
            <div class="agent-title">Content Strategist</div>
            <div class="agent-desc">Creates brand voice guidelines, content pillars, editorial calendar, and sample content drafts.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">📈</div>
            <div class="agent-title">Analytics Specialist</div>
            <div class="agent-desc">Sets up KPI frameworks, tracking plans, dashboard designs, and attribution models.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">⚡</div>
            <div class="agent-title">Optimization Advisor</div>
            <div class="agent-desc">Reviews the strategy, suggests quick wins, A/B tests, budget optimization, and readiness scoring.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture Flow
    st.markdown("")
    st.markdown("### 🔄 Agent Architecture Flow")
    st.markdown("""
    <div class="flow-container">
        <span class="flow-step">📥 Business Input</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">📊 Market Research</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">🏢 Competitor Analysis</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">📋 Campaign Planning</span>
        <br><br>
        <span class="flow-step">📋 Campaign Planning</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">✍️ Content Strategy</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">📈 Analytics</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">⚡ Optimization</span>
        <span class="flow-arrow">→</span>
        <span class="flow-step">📤 Final Strategy</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("")
    st.markdown("### ✨ Key Features")
    
    feat_col1, feat_col2 = st.columns(2)
    with feat_col1:
        st.markdown("""
        - 🤖 **6 Specialized AI Agents** working in coordination
        - 🔍 **Real-time Web Research** using DuckDuckGo
        - 📈 **Trend Analysis** with live market data
        - 🏢 **SEO Analysis** of competitor websites
        - 🤝 **Human-in-the-Loop** approval for campaigns
        """)
    with feat_col2:
        st.markdown("""
        - ⚡ **Powered by Groq** for ultra-fast inference
        - 🧠 **Shared Context** memory across agents
        - 📊 **Structured Outputs** from each agent
        - 📥 **Downloadable Reports** in text format
        - 🔒 **Secure** - API key stored only in session
        """)
    
    st.markdown("")
    st.info("👈 Enter your business details in the sidebar and click **Generate Marketing Strategy** to get started!")
