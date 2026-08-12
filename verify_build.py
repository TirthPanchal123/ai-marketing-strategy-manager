import sys
import os

# Set dummy key for verification
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = "verify-mock-key"

print("Verifying project build files...")
try:
    print("1. Importing tools...")
    import tools
    print("   Tools imported successfully.")
    
    print("2. Importing agents_config...")
    import agents_config
    print("   Agents imported and wired successfully.")
    print("   Available Agents:", [
        agents_config.triage_agent.name,
        agents_config.market_research_agent.name,
        agents_config.competitor_analysis_agent.name,
        agents_config.campaign_planner_agent.name,
        agents_config.content_strategist_agent.name,
        agents_config.optimisation_advisor_agent.name
    ])
    
    print("3. Testing budget_forecaster_tool directly...")
    res = tools.calculate_budget_forecast(10000, "SaaS", "Balanced")
    print("   Result keys:", res.keys())
    assert "channel_splits" in res
    assert "aggregate_metrics" in res
    print("   Budget Forecaster works correctly.")
    
    print("4. Testing ppt_presentation_tool directly (generating verification PPTX)...")
    ppt_path = tools.generate_ppt_presentation(
        "VerificationBrand", "SaaS",
        "Market Research Details...",
        "Competitor analysis...",
        "Campaign strategy...",
        "Content copywriting...",
        "Budget forecasting..."
    )
    print("   PPT slide-deck generated at:", ppt_path)
    assert os.path.exists(ppt_path)
    print("   PPT presentation tool works correctly.")
    
    print("5. Testing marketing_report_tool directly...")
    rep_path = tools.generate_marketing_report("VerificationBrand", "Research findings and campaign strategy details...")
    print("   Markdown report generated at:", rep_path)
    assert os.path.exists(rep_path)
    print("   Marketing report tool works correctly.")
    
    print("SUCCESS: All verification checks passed!")
    sys.exit(0)
except Exception as e:
    print("ERROR: Verification failed:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
