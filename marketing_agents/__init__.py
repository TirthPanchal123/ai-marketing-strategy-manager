"""
AI Marketing Strategy Manager - Specialized Marketing Agents.

This package contains the project's custom marketing agents while also
exposing the installed OpenAI Agents SDK from the same namespace.
"""

import os
import site

# ============================================================
# PACKAGE PATH SETUP
# ============================================================

_LOCAL_AGENTS_PATH = os.path.abspath(os.path.dirname(__file__))

_installed_agents_path = None

for base_path in site.getsitepackages() + [site.getusersitepackages()]:
    candidate = os.path.join(base_path, "agents")

    if (
        os.path.isdir(candidate)
        and os.path.abspath(candidate) != _LOCAL_AGENTS_PATH
    ):
        _installed_agents_path = os.path.abspath(candidate)
        break


# IMPORTANT:
# Put the installed OpenAI Agents SDK FIRST.
#
# This makes:
#     agents.model_settings
#     agents.agent
#     agents.run
# etc.
#
# come from the installed OpenAI Agents SDK instead of the local
# project folder.
#
# Our custom files such as:
#     agents.market_research_agent
#     agents.campaign_planner_agent
#     agents.orchestrator
#
# are still available from the local folder.

if _installed_agents_path:
    __path__ = [
        _installed_agents_path,
        _LOCAL_AGENTS_PATH,
    ]
else:
    __path__ = [
        _LOCAL_AGENTS_PATH,
    ]


# ============================================================
# OPENAI AGENTS SDK EXPORTS
# ============================================================

try:
    from agents.agent import Agent
except ImportError:
    Agent = None

try:
    from agents.run import Runner
except ImportError:
    Runner = None

try:
    from agents.handoffs import handoff
except ImportError:
    handoff = None

try:
    from agents.tool import function_tool
except ImportError:
    try:
        from marketing_agents import function_tool
    except ImportError:
        function_tool = None

try:
    from agents.model_settings import ModelSettings
except ImportError:
    ModelSettings = None


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "Agent",
    "Runner",
    "handoff",
    "function_tool",
    "ModelSettings",
]