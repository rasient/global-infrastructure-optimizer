from __future__ import annotations

import os
from typing import Dict, List


class OpenAIAnalysisService:
    """AI-assisted recommendation service.

    The MVP uses mock output so the app runs without API keys.
    Later, connect this to the OpenAI API for richer structured analysis.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.mock_mode = os.getenv("USE_MOCK_MODE", "true").lower() == "true"

    def analyze_profile(self, profile: Dict, gaps: List[str], recommendations: List[str]) -> str:
        city = profile.get("city", "the selected city")

        if self.mock_mode or not self.api_key:
            gap_text = "\n".join(f"- {gap}" for gap in gaps)
            rec_text = "\n".join(f"- {rec}" for rec in recommendations)
            return f"""# Infrastructure System Diagnosis: {city}

## Core interpretation
{city}'s mobility system should be treated as a portfolio of transport modes, not a competition between individual modes.

## Main gaps
{gap_text}

## Recommendations
{rec_text}

## Key system question
How well do transport modes work together when people actually move through the city under real conditions?
"""

        # Minimal safe placeholder for future API integration.
        # Add OpenAI SDK call here once keys and model choice are configured.
        raise NotImplementedError("Real OpenAI integration is planned in the roadmap.")
