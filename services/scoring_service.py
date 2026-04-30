from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TransportScore:
    category: str
    score: int
    explanation: str


def score_city_profile(profile: Dict) -> List[TransportScore]:
    """Create simple MVP scores from a city profile.

    This is intentionally heuristic. Later versions can replace this with
    real map data, route matrices, emissions factors, and capacity models.
    """
    strengths = profile.get("strengths", [])
    weaknesses = profile.get("weaknesses", [])
    modes = profile.get("dominant_modes", [])

    integration_score = max(30, min(90, 70 + len(strengths) * 3 - len(weaknesses) * 5))
    resilience_score = max(25, min(90, 50 + len(modes) * 5 - len(weaknesses) * 3))
    accessibility_score = max(25, min(90, 55 + ("walking" in modes) * 10 + ("bus" in modes) * 8 - len(weaknesses) * 2))

    return [
        TransportScore(
            category="Multimodal Integration",
            score=int(integration_score),
            explanation="How well different transport modes appear to connect into one usable system.",
        ),
        TransportScore(
            category="System Resilience",
            score=int(resilience_score),
            explanation="How many alternative modes exist when one part of the system is overloaded or fails.",
        ),
        TransportScore(
            category="Accessibility",
            score=int(accessibility_score),
            explanation="How easily people can access mobility without relying only on private cars.",
        ),
    ]


def identify_system_gaps(profile: Dict) -> List[str]:
    weaknesses = profile.get("weaknesses", [])
    gaps = []

    for weakness in weaknesses:
        gaps.append(f"Potential system gap: {weakness}.")

    if "cycling" not in profile.get("dominant_modes", []):
        gaps.append("Cycling may be underrepresented in the current mode portfolio.")

    if "walking" not in profile.get("dominant_modes", []):
        gaps.append("Walking access should be assessed as the foundation of all trips.")

    return gaps


def generate_recommendations(profile: Dict) -> List[str]:
    opportunities = profile.get("opportunities", [])
    city = profile.get("city", "this city")

    recommendations = [
        f"Map the strongest and weakest transfer points in {city}.",
        "Prioritize interfaces between modes, not only individual transport assets.",
        "Score projects by system-level impact: access, emissions, capacity, and resilience.",
    ]

    for opportunity in opportunities:
        recommendations.append(f"Explore opportunity: {opportunity}.")

    return recommendations
