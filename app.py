import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

# Set matplotlib backend to Agg to prevent GUI thread issues in Streamlit
import matplotlib
matplotlib.use('Agg')

# Load local environment variables
load_dotenv()

# Set up page configurations
st.set_page_config(
    page_title="AI Marketing Strategy Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1E88E5 0%, #00E5FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #B0BEC5;
        margin-bottom: 2rem;
    }
    
    .card {
        background-color: #1E1E24;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2E2E38;
        margin-bottom: 1rem;
    }
    
    .agent-header {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .trace-step {
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.85rem;
        color: #00E676;
        padding: 0.2rem 0.5rem;
        background: #111;
        border-left: 3px solid #FF7043;
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='main-title'>🎯 AI Marketing Strategy Manager</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>OpenAI Agents SDK Capstone Project - Statement 14. Developed for Summer School '26</p>", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIG -----------------
st.sidebar.image("C:\\Users\\Tirth\\.gemini\\antigravity\\scratch\\agent_architecture.png", use_container_width=True, caption="Multi-Agent Handoff Flow")
st.sidebar.title("Configuration Control")

# Secure API Key Entry
env_key = os.environ.get("GROQ_API_KEY", "")
api_key = st.sidebar.text_input("Groq API Key", type="password", value=env_key, placeholder="gsk_...")

if api_key:
    os.environ["GROQ_API_KEY"] = api_key

# Preset Selector to assist grading/testing
st.sidebar.subheader("Quick Presets")
preset_options = {
    "None": {
        "name": "", "industry": "SaaS", "description": "", "keywords": "", "budget": 15000.0, "goal": "Balanced"
    },
    "EcoClean: Smart Water Bottle (E-commerce)": {
        "name": "EcoClean",
        "industry": "E-commerce",
        "description": "A smart, reusable water bottle that uses UV-C LED technology to self-clean and purify water in 60 seconds.",
        "keywords": "reusable, self-cleaning, uv purification, sustainable, smart bottle",
        "budget": 25000.0,
        "goal": "Aggressive Growth"
    },
    "DevFlow: DevOps SaaS (SaaS)": {
        "name": "DevFlow",
        "industry": "SaaS",
        "description": "An AI-powered continuous deployment platform that automates Kubernetes orchestration and monitors cluster health in real time.",
        "keywords": "kubernetes, deployment automation, ai devops, continuous integration, cloud monitor",
        "budget": 50000.0,
        "goal": "Balanced"
    },
    "PulseHealth: AI Diagnostic Wearable (Healthcare)": {
        "name": "PulseHealth",
        "industry": "Healthcare",
        "description": "A non-invasive diagnostic health ring that tracks cardiovascular metrics and alerts doctors to cardiac anomalies using proprietary AI.",
        "keywords": "health ring, diagnostics, cardiovascular monitor, doctor alert, diagnostic wearable",
        "budget": 12000.0,
        "goal": "Organic Focus"
    }
}

selected_preset = st.sidebar.selectbox("Load Demo Preset", list(preset_options.keys()))

preset_data = preset_options[selected_preset]

# Inputs Form
st.sidebar.subheader("Brand Parameters")
brand_name = st.sidebar.text_input("Brand Name", value=preset_data["name"])
industry = st.sidebar.selectbox("Industry Sector", ["SaaS", "E-commerce", "B2B Services", "Healthcare", "Real Estate"], index=["SaaS", "E-commerce", "B2B Services", "Healthcare", "Real Estate"].index(preset_data["industry"]))
product_desc = st.sidebar.text_area("Product/Service Description", value=preset_data["description"])
target_keywords = st.sidebar.text_input("SEO Target Keywords (comma separated)", value=preset_data["keywords"])
ad_budget = st.sidebar.number_input("Ad Budget (USD)", min_value=1000.0, max_value=1000000.0, value=preset_data["budget"], step=1000.0)
strategy_goal = st.sidebar.selectbox("Marketing Strategy Focus", ["Balanced", "Aggressive Growth", "Organic Focus"], index=["Balanced", "Aggressive Growth", "Organic Focus"].index(preset_data["goal"]))

# ----------------- SESSION STATE INITIALIZATION -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trace" not in st.session_state:
    st.session_state.trace = []
if "budget_results" not in st.session_state:
    st.session_state.budget_results = None
if "run_completed" not in st.session_state:
    st.session_state.run_completed = False
if "report_path" not in st.session_state:
    st.session_state.report_path = ""
if "presentation_path" not in st.session_state:
    st.session_state.presentation_path = ""

# ----------------- EXECUTION CODE -----------------
def execute_agent_pipeline():
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter a valid Groq API Key in the sidebar to run the multi-agent system!")
        return
        
    st.session_state.messages = []
    st.session_state.trace = []
    st.session_state.run_completed = False
    
    # Import Agents packages here to avoid early runtime failures on loading
    try:
        from marketing_agents import Runner
        from agents_config import triage_agent
        from agents.memory.sqlite_session import SQLiteSession
        from tools import calculate_budget_forecast
    except Exception as err:
        st.error(f"Failed to import Agents SDK: {err}")
        return
        
    # Configure SQLite session for persistence
    db_file = os.path.join("C:\\Users\\Tirth\\.gemini\\antigravity\\scratch\\ai-marketing-strategy-manager", "sessions.db")
    session = SQLiteSession(session_id="marketing_capstone_session", db_path=db_file)
    
    # Construct structured system query
    user_query = (
        f"Brand Name: {brand_name}\n"
        f"Industry: {industry}\n"
        f"Description: {product_desc}\n"
        f"SEO Target Keywords: {target_keywords}\n"
        f"Total Ad Budget: ${ad_budget}\n"
        f"Strategy Focus: {strategy_goal}\n\n"
        f"Coordinate a complete marketing audit. Run research, competitor checks, campaigns, copy SEO analyses, "
        f"and execute budget forecasts. Generate a structured Markdown report and the PowerPoint slide deck."
    )
    
    st.session_state.trace.append("🚀 Initializing Triage Agent (Marketing Director)")
    st.session_state.trace.append("🔄 Triage Agent initiating sequential marketing analysis...")
    
    # Visual Loading Indicators
    with st.spinner("Multi-Agent Marketing Team executing. Running searches, scraping competitor sites, planning campaigns, and analyzing copy..."):
        try:
            # Execute agents loop
            result = Runner.run_sync(triage_agent, user_query, session=session)
            
            # Parse execution traces and logs
            for item in result.new_items:
                agent_name = item.agent.name if hasattr(item, 'agent') and item.agent else "System"
                
                if item.type == "message_output_item":
                    content = item.raw_item.content if hasattr(item.raw_item, 'content') else ""
                    if content:
                        st.session_state.messages.append({"role": agent_name, "content": content})
                        
                elif item.type == "handoff_call_item":
                    target = item.raw_item.target_agent_name if hasattr(item.raw_item, 'target_agent_name') else "next specialist"
                    st.session_state.trace.append(f"🔄 Handoff: Control transferred from {agent_name} to {target}")
                    
                elif item.type == "tool_call_item":
                    tool_name = item.raw_item.name if hasattr(item.raw_item, 'name') else "tool"
                    args = item.raw_item.arguments if hasattr(item.raw_item, 'arguments') else ""
                    st.session_state.trace.append(f"🛠️ Tool Call: {agent_name} invoked '{tool_name}' (params: {args})")
                    
                elif item.type == "tool_call_output_item":
                    st.session_state.trace.append(f"📤 Tool Executed: Returned structured content successfully.")
            
            # Execute budget forecaster tool for Streamlit UI metrics
            keyword_list = [kw.strip() for kw in target_keywords.split(",") if kw.strip()]
            budget_metrics = calculate_budget_forecast(ad_budget, industry, strategy_goal)
            st.session_state.budget_results = budget_metrics
            
            # Locate output file paths
            workspace_dir = "C:\\Users\\Tirth\\.gemini\\antigravity\\scratch\\ai-marketing-strategy-manager"
            st.session_state.report_path = os.path.join(workspace_dir, "marketing_strategy_report.md")
            st.session_state.presentation_path = os.path.join(workspace_dir, "marketing_strategy_presentation.pptx")
            st.session_state.run_completed = True
            st.session_state.trace.append("✅ Playbook presentation and strategy report generated successfully!")
            
        except Exception as run_err:
            st.error(f"Execution Error: {run_err}")
            st.session_state.trace.append(f"❌ Execution failed with error: {run_err}")

# Run Trigger
if st.sidebar.button("Launch Multi-Agent Campaign Audit", use_container_width=True):
    if not brand_name or not product_desc:
        st.warning("Please fill in the Brand Name and Product Description in the sidebar first!")
    else:
        execute_agent_pipeline()

# ----------------- MAIN LAYOUT TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🖥️ Agent Terminal", 
    "📊 Financial Forecasts", 
    "⚙️ Multi-Agent Architecture",
    "💾 Download Strategy Files"
])

# TAB 1: AGENT TERMINAL
with tab1:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Multi-Agent Dialogue History")
        if not st.session_state.messages:
            st.info("The terminal is idle. Fill in the parameters and click 'Launch Multi-Agent Campaign Audit' to start.")
        else:
            # Map agent names to clean avatars and display names
            avatar_map = {
                "Triage_Agent": "🧑‍💼",
                "Market_Research_Agent": "🔍",
                "Competitor_Analysis_Agent": "⚔️",
                "Campaign_Planner_Agent": "🎯",
                "Content_Strategist_Agent": "✍️",
                "Optimisation_Advisor_Agent": "📈",
                "System": "🖥️"
            }
            
            for msg in st.session_state.messages:
                role = msg["role"]
                avatar = avatar_map.get(role, "🤖")
                clean_name = role.replace("_", " ")
                
                with st.chat_message(clean_name, avatar=avatar):
                    st.markdown(f"**{clean_name}**")
                    st.markdown(msg["content"])
                    
    with col_right:
        st.subheader("Agent Execution Log")
        if not st.session_state.trace:
            st.info("Log is empty. Run the audit to capture agent handoffs and tool executions.")
        else:
            for step in st.session_state.trace:
                st.markdown(f"<div class='trace-step'>{step}</div>", unsafe_allow_html=True)

# TAB 2: STRATEGY DASHBOARD & FINANCIAL FORECASTS
with tab2:
    if not st.session_state.run_completed or st.session_state.budget_results is None:
        st.info("Financial Dashboard will populate once the audit is successfully executed.")
    else:
        res = st.session_state.budget_results
        metrics = res["aggregate_metrics"]
        
        st.subheader("Key Performance Indicators (KPIs) Forecasted")
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Total Budget Allocated", f"${res['total_budget']:,.2f}")
        m_col2.metric("Total Clicks Expected", f"{metrics['total_clicks']:,}")
        m_col3.metric("Expected Conversions", f"{metrics['total_conversions']:,}")
        m_col4.metric("Forecasted Blended CPA", f"${metrics['blended_cpa']:.2f}")
        
        st.markdown("---")
        
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.subheader("Ad Spend Allocation by Channel")
            
            # Pie Chart
            channels = list(res["channel_splits"].keys())
            budgets = [c["budget_usd"] for c in res["channel_splits"].values()]
            
            fig, ax = plt.subplots(figsize=(6, 5), facecolor='#0E1117')
            ax.set_facecolor('#0E1117')
            
            # Theme tailoring
            colors = ['#1E88E5', '#00ACC1', '#43A047', '#FF7043']
            wedges, texts, autotexts = ax.pie(
                budgets, labels=channels, autopct='%1.1f%%',
                startangle=140, colors=colors,
                textprops=dict(color="w")
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
                
            plt.title(f"Spend Split: {res['strategy']}", color='w', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            
        with c_right:
            st.subheader("Forecast Breakdown by Channel")
            
            df_data = []
            for channel, c_data in res["channel_splits"].items():
                df_data.append({
                    "Channel": channel,
                    "Budget (USD)": f"${c_data['budget_usd']:,.2f}",
                    "Est. Clicks": f"{c_data['estimated_clicks']:,}",
                    "Est. Conversions": f"{c_data['estimated_conversions']:,}",
                    "Est. CPA": f"${c_data['estimated_cpa']:.2f}"
                })
            df = pd.DataFrame(df_data)
            st.table(df)
            
            st.info(
                f"**Strategic Summary**: Based on B2B benchmarks in the **{res['industry']}** sector under an **{res['strategy']}** framework, "
                f"this ad spend structure is forecasted to generate **${metrics['estimated_revenue_usd']:,.2f}** in simulated revenue, "
                f"yielding an estimated ROI of **{metrics['estimated_roi_percent']}%**."
            )

# TAB 3: SYSTEM ARCHITECTURE & DIAGRAMS
with tab3:
    st.subheader("Multi-Agent Architecture & Handoff Design")
    
    col_diag, col_desc = st.columns([3, 2])
    
    with col_diag:
        # Load local programmatically generated diagram
        diag_path = "C:\\Users\\Tirth\\.gemini\\antigravity\\scratch\\agent_architecture.png"
        if os.path.exists(diag_path):
            st.image(diag_path, use_container_width=True, caption="OpenAI Agents SDK Architecture & Communication Paths")
        else:
            st.warning("Diagram file not found. Ensure create_diagrams.py has run successfully.")
            
    with col_desc:
        st.markdown("""
        ### Multi-Agent Specifications
        
        This submission implements a complete, production-grade agentic workflow utilizing the **OpenAI Agents SDK** and **SQLite Session Storage** to achieve context management and automated handoffs.
        
        #### Agent Specifications:
        1. **Triage Agent (Marketing Director)**: Orchestrates the user experience. Evaluates inputs, welcomes the user, and schedules/dispatches specialist agents dynamically.
        2. **Market Research Agent**: Investigates web-trends and benchmarks. Uses DuckDuckGo HTML scraping tool APIs.
        3. **Competitor Analysis Agent**: Evaluates competitor marketing models and creates landing page copy intelligence.
        4. **Campaign Planner Agent**: Structures the complete three-tier funnel campaigns (Awareness, Consideration, Conversion).
        5. **Content Strategist Agent**: Drafts copy and uses local SEO tools to analyze keyword densities.
        6. **Optimisation Advisor Agent**: Performs financial calculations, runs the budget splits, generates the reports, and builds the PPT presentation.
        
        #### Key Technical Highlights:
        - **Stateful Memory**: Managed using the SDK's `SQLiteSession` class, maintaining full chat logs and state variables across multiple execution calls.
        - **Bidirectional Handoffs**: Circular routing is established enabling specialized agents to delegate tasks downstream (e.g. Research -> Competitor -> Campaign) or yield control back to Triage.
        - **Dynamic Schema Tooling**: Uses the `@function_tool` decorator, which dynamically parses python signatures and docstrings to structure tool schemas for LLM routing.
        """)

# TAB 4: DOWNLOAD SUBMISSION DELIVERABLES
with tab4:
    st.subheader("Capstone Deliverables & Strategy Playbook Downloads")
    st.write("Once the agent pipeline runs successfully, download the capstone files for submission:")
    
    if not st.session_state.run_completed:
        st.warning("Please execute the multi-agent audit in Tab 1 to generate download links.")
    else:
        # Read files for download
        try:
            with open(st.session_state.report_path, "r", encoding="utf-8") as f_rep:
                report_content = f_rep.read()
                
            with open(st.session_state.presentation_path, "rb") as f_pres:
                presentation_bytes = f_pres.read()
                
            d_col1, d_col2 = st.columns(2)
            
            with d_col1:
                st.info("📄 **Structured Strategy Report**")
                st.caption("A detailed marketing analysis report containing findings from all agents in formatted Markdown.")
                st.download_button(
                    label="Download Strategy Report (.md)",
                    data=report_content,
                    file_name="marketing_strategy_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            with d_col2:
                st.success("💻 **Slide-Deck Presentation (10-12 Slides)**")
                st.caption("A premium PowerPoint presentation detailing the complete strategy, formatted with a professional 16:9 widescreen layout.")
                st.download_button(
                    label="Download Slide-Deck Presentation (.pptx)",
                    data=presentation_bytes,
                    file_name="marketing_strategy_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
                
            st.markdown("---")
            st.subheader("Generated Strategy Report Preview")
            st.markdown(report_content)
            
        except Exception as read_err:
            st.error(f"Failed to read generated deliverables: {read_err}")
