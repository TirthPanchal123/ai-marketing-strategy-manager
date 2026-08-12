import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_diagram():
    # Set up figure
    fig, ax = plt.subplots(figsize=(15, 9), facecolor='#121214')
    ax.set_facecolor('#121214')
    
    # Define colors
    c_bg = '#1E1E24'
    c_triage = '#1E88E5'      # Vivid Blue
    c_specialist = '#00B0FF'  # Sky Blue
    c_secondary = '#00E5FF'   # Bright Cyan/Teal
    c_tool = '#00E676'        # Green Accent
    c_text = '#FFFFFF'
    c_subtext = '#B0BEC5'
    c_line = '#FF7043'        # Coral for flow
    
    # 1. Triage Agent (Center)
    # Box parameters: x, y, width, height
    triage_box = patches.FancyBboxPatch(
        (6.0, 4.0), 3.0, 1.5, 
        boxstyle="round,pad=0.2", 
        linewidth=2, edgecolor=c_triage, facecolor=c_bg
    )
    ax.add_patch(triage_box)
    ax.text(7.5, 4.75, "TRIAGE AGENT\n(Marketing Director)", 
            color=c_text, fontsize=12, fontweight='bold', ha='center', va='center')
    
    # 2. Market Research Agent (Top Left)
    res_box = patches.FancyBboxPatch(
        (1.5, 6.5), 2.5, 1.2, 
        boxstyle="round,pad=0.2", 
        linewidth=1.5, edgecolor=c_specialist, facecolor=c_bg
    )
    ax.add_patch(res_box)
    ax.text(2.75, 7.1, "MARKET RESEARCH AGENT\n(Industry Trends)", 
            color=c_text, fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(2.75, 6.75, "Tool: search_web_tool", 
            color=c_tool, fontsize=8, ha='center', va='center')
    
    # 3. Competitor Analysis Agent (Top Right)
    comp_box = patches.FancyBboxPatch(
        (10.5, 6.5), 2.5, 1.2, 
        boxstyle="round,pad=0.2", 
        linewidth=1.5, edgecolor=c_specialist, facecolor=c_bg
    )
    ax.add_patch(comp_box)
    ax.text(11.75, 7.1, "COMPETITOR ANALYST\n(Competitive Maps)", 
            color=c_text, fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(11.75, 6.75, "Tools: search_web_tool\nfetch_url_metadata", 
            color=c_tool, fontsize=8, ha='center', va='center')
            
    # 4. Campaign Planner Agent (Bottom Right)
    camp_box = patches.FancyBboxPatch(
        (10.5, 1.5), 2.5, 1.2, 
        boxstyle="round,pad=0.2", 
        linewidth=1.5, edgecolor=c_specialist, facecolor=c_bg
    )
    ax.add_patch(camp_box)
    ax.text(11.75, 2.1, "CAMPAIGN PLANNER\n(Strategy & Timelines)", 
            color=c_text, fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(11.75, 1.75, "Tool: search_web_tool", 
            color=c_tool, fontsize=8, ha='center', va='center')
            
    # 5. Content Strategist Agent (Bottom Left)
    content_box = patches.FancyBboxPatch(
        (1.5, 1.5), 2.5, 1.2, 
        boxstyle="round,pad=0.2", 
        linewidth=1.5, edgecolor=c_specialist, facecolor=c_bg
    )
    ax.add_patch(content_box)
    ax.text(2.75, 2.1, "CONTENT STRATEGIST\n(Copy & Keyword Density)", 
            color=c_text, fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(2.75, 1.75, "Tool: seo_analyzer_tool", 
            color=c_tool, fontsize=8, ha='center', va='center')
            
    # 6. Optimisation Advisor Agent (Center Bottom)
    opt_box = patches.FancyBboxPatch(
        (6.0, 1.0), 3.0, 1.3, 
        boxstyle="round,pad=0.2", 
        linewidth=1.5, edgecolor=c_specialist, facecolor=c_bg
    )
    ax.add_patch(opt_box)
    ax.text(7.5, 1.65, "OPTIMISATION ADVISOR\n(Financials & Deliverables)", 
            color=c_text, fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(7.5, 1.25, "Tools: budget_forecaster_tool\nppt_presentation_tool, marketing_report_tool", 
            color=c_tool, fontsize=8, ha='center', va='center')

    # Draw Arrows & Handoff Paths
    # Double-headed arrow styles for handoffs back and forth
    arrow_props = dict(arrowstyle="<->", color=c_line, lw=1.5, mutation_scale=15)
    sequence_arrow = dict(arrowstyle="->", color=c_line, lw=2, ls='--', mutation_scale=15)
    
    # User Input arrow
    ax.annotate("User Prompt", xy=(6.0, 4.75), xytext=(4.2, 4.75),
                arrowprops=dict(arrowstyle="->", color='#FFFFFF', lw=2),
                color='#FFFFFF', fontsize=10, fontweight='bold', ha='center')
                
    # Final Output arrow
    ax.annotate("Strategy Report & PPTX", xy=(10.8, 4.75), xytext=(9.0, 4.75),
                arrowprops=dict(arrowstyle="->", color='#FFFFFF', lw=2),
                color='#FFFFFF', fontsize=10, fontweight='bold', ha='center')
                
    # Handoffs: Triage <-> Specialists
    ax.annotate("", xy=(3.5, 6.5), xytext=(6.2, 5.2), arrowprops=arrow_props) # Triage <-> Research
    ax.annotate("", xy=(11.0, 6.5), xytext=(8.8, 5.2), arrowprops=arrow_props) # Triage <-> Competitor
    ax.annotate("", xy=(11.0, 2.7), xytext=(8.8, 4.3), arrowprops=arrow_props) # Triage <-> Campaign
    ax.annotate("", xy=(3.5, 2.7), xytext=(6.2, 4.3), arrowprops=arrow_props) # Triage <-> Content
    ax.annotate("", xy=(7.5, 2.3), xytext=(7.5, 4.0), arrowprops=arrow_props) # Triage <-> Optimisation
    
    # Sequential Pipeline (dotted circles)
    ax.annotate("Research Handoff", xy=(10.5, 7.1), xytext=(4.0, 7.1), arrowprops=sequence_arrow, color=c_subtext, fontsize=8, va='center')
    ax.annotate("Competitor Handoff", xy=(11.75, 2.7), xytext=(11.75, 6.5), arrowprops=sequence_arrow, color=c_subtext, fontsize=8, ha='center')
    ax.annotate("Campaign Handoff", xy=(4.0, 2.1), xytext=(10.5, 2.1), arrowprops=sequence_arrow, color=c_subtext, fontsize=8, va='center')
    ax.annotate("Copy Handoff", xy=(7.5, 1.0), xytext=(2.75, 1.5), arrowprops=sequence_arrow, color=c_subtext, fontsize=8, va='center')
    
    # Graph titles and notes
    ax.text(7.5, 8.4, "AI MARKETING STRATEGY PLATFORM", color='#FFFFFF', fontsize=18, fontweight='bold', ha='center')
    ax.text(7.5, 8.0, "Multi-Agent System Architecture & Interaction Flow (OpenAI Agents SDK)", 
            color=c_secondary, fontsize=12, ha='center')
    
    # Legend
    ax.add_patch(patches.Rectangle((0.5, 0.2), 0.3, 0.15, facecolor=c_bg, edgecolor=c_triage, lw=1.5))
    ax.text(0.9, 0.275, "Orchestrator Agent", color=c_text, fontsize=8, va='center')
    
    ax.add_patch(patches.Rectangle((3.0, 0.2), 0.3, 0.15, facecolor=c_bg, edgecolor=c_specialist, lw=1.5))
    ax.text(3.4, 0.275, "Specialist Agents", color=c_text, fontsize=8, va='center')
    
    ax.add_patch(patches.Rectangle((5.5, 0.2), 0.3, 0.15, facecolor=c_bg, edgecolor=c_tool, lw=1.5))
    ax.text(5.9, 0.275, "Associated Tools/APIs", color=c_text, fontsize=8, va='center')
    
    ax.annotate("", xy=(8.7, 0.275), xytext=(8.0, 0.275), arrowprops=dict(arrowstyle="<->", color=c_line, lw=1.5))
    ax.text(8.8, 0.275, "Handoff Delegation", color=c_text, fontsize=8, va='center')
    
    ax.annotate("", xy=(11.7, 0.275), xytext=(11.0, 0.275), arrowprops=dict(arrowstyle="->", color=c_line, lw=1.5, ls='--'))
    ax.text(11.8, 0.275, "Sequential Pipeline", color=c_text, fontsize=8, va='center')
    
    # Remove axes
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Save diagram
    dir_path = "C:\\Users\\Tirth\\.gemini\\antigravity\\scratch\\ai-marketing-strategy-manager"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_path = os.path.join(dir_path, "agent_architecture.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#121214')
    plt.close()
    print(f"Diagram saved successfully to {save_path}")

if __name__ == "__main__":
    generate_diagram()
