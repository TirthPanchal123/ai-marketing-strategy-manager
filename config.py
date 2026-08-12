"""
Configuration module for AI Marketing Strategy Manager.
Uses Groq through the OpenAI-compatible Chat Completions API.
Compatible with openai-agents 0.18.3
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

MAIN_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

FAST_MODEL = "llama-3.1-8b-instant"


# ============================================================
# GROQ CLIENT
# ============================================================

def get_groq_client():
    """
    Create an AsyncOpenAI client configured for Groq.
    """

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is missing.\n"
            "Add GROQ_API_KEY=your_key to the .env file."
        )

    return AsyncOpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
    )


# ============================================================
# AGENTS SDK MODEL
# ============================================================

def get_model(model_name: str = MAIN_MODEL):
    """
    Return an OpenAI Agents SDK model configured for Groq.

    openai-agents 0.18.3 compatible implementation.
    """

    from agents.models.openai_chatcompletions import (
        OpenAIChatCompletionsModel
    )

    client = get_groq_client()

    return OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=client,
    )


# ============================================================
# FAST MODEL
# ============================================================

def get_fast_model():
    """
    Return the fast Groq model.
    """

    return get_model(FAST_MODEL)


# ============================================================
# UPDATE API KEY
# ============================================================

def update_api_key(api_key: str):
    """
    Update Groq API key at runtime.
    """

    global GROQ_API_KEY

    GROQ_API_KEY = api_key.strip()

    if GROQ_API_KEY:
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY