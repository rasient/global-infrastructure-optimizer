from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TransportScore:
    category: str
    score: int
    explanation: str


@dataclass
class InterfaceScore:
    connection: str
    friction: float
    score: int
    issue: str


SYSTEM_DIMENSIONS = [
    "capacity",
    "speed",
    "coverage",
    "emissions",
    "accessibility",
    "resilience",
]


def clamp(value: float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def score_city_profile(profile: Dict) -> List[TransportScore]:
    strengths = profile.get("strengths", [])
    weaknesses = profile.get("weaknesses", [])
    modes = profile.get("dominant_modes", [])
    interfaces = profile.get("interfaces", [])
    mode_scores = profile.get("mode_scores", {})

    if mode_scores:
        dimension_averages = []
        for mode_data in mode_scores.values():
            values = [mode_data.get(d, 50) for d in SYSTEM_DIMENSIONS]
            dimension_averages.append(sum(values) / len(values))
        mode_portfolio_score = sum(dimension_averages) / len(dimension_averages)
    else:
        mode_portfolio_score = 55 + len(modes) * 3

    avg_friction = sum(i.get("friction", 0.5) for i in interfaces) / max(1, len(interfaces))
    interface_score = 100 * (1 - avg_friction)

    layer_count = len(profile.get("layers", {}))
    resilience_score = 45 + len(modes) * 3 + layer_count * 4 - len(weaknesses) * 3
    accessibility_score = (
        55
        + ("walking" in modes) * 10
        + ("bicycle" in modes or "cycling" in modes) * 8
        + ("bus" in modes) * 6
        - avg_friction * 12
    )
    coordination_score = 60 + len(strengths) * 3 - len(weaknesses) * 4 - avg_friction * 18

    return [
        TransportScore(
            category="Mode Portfolio",
            score=clamp(mode_portfolio_score),
            explanation="How strong the available transport modes are across capacity, coverage, emissions, accessibility, and resilience.",
        ),
        TransportScore(
            category="Interface Quality",
            score=clamp(interface_score),
            explanation="How much friction exists between modes when people move through the system.",
        ),
        TransportScore(
            category="System Coordination",
            score=clamp(coordination_score),
            explanation="How well the transport portfolio behaves as one coordinated mobility system.",
        ),
        TransportScore(
            category="System Resilience",
            score=clamp(resilience_score),
            explanation="How many alternatives exist when one layer is overloaded or disrupted.",
        ),
        TransportScore(
            category="Accessibility",
            score=clamp(accessibility_score),
            explanation="How easily people can use the system without relying only on private cars.",
        ),
    ]


def score_interfaces(profile: Dict) -> List[InterfaceScore]:
    scores: List[InterfaceScore] = []
    for interface in profile.get("interfaces", []):
        friction = float(interface.get("friction", 0.5))
        scores.append(
            InterfaceScore(
                connection=f"{interface.get('from', 'unknown')} → {interface.get('to', 'unknown')}",
                friction=friction,
                score=clamp(100 * (1 - friction)),
                issue=interface.get("issue", "No issue specified"),
            )
        )
    return sorted(scores, key=lambda item: item.score)


def mode_portfolio_table(profile: Dict) -> List[Dict]:
    rows = []
    for mode, values in profile.get("mode_scores", {}).items():
        avg = sum(values.values()) / max(1, len(values))
        rows.append({"mode": mode, "overall": clamp(avg), **values})
    return sorted(rows, key=lambda row: row["overall"], reverse=True)


def identify_system_gaps(profile: Dict) -> List[str]:
    weaknesses = profile.get("weaknesses", [])
    modes = profile.get("dominant_modes", [])
    interfaces = score_interfaces(profile)
    gaps = []

    for weakness in weaknesses:
        gaps.append(f"Potential system gap: {weakness}.")

    if "bicycle" not in modes and "cycling" not in modes:
        gaps.append("Cycling or bike-to-transit access may be underrepresented in the current mode portfolio.")

    if "walking" not in modes:
        gaps.append("Walking access should be assessed as the foundation of all trips.")

    for interface in interfaces[:3]:
        gaps.append(f"High-friction interface: {interface.connection} — {interface.issue}.")

    return gaps


def generate_recommendations(profile: Dict) -> List[str]:
    opportunities = profile.get("opportunities", [])
    city = profile.get("city", "this city")
    weakest_interfaces = score_interfaces(profile)[:2]

    recommendations = [
        f"Map the strongest and weakest transfer points in {city}.",
        "Prioritize interfaces between modes, not only individual transport assets.",
        "Score projects by system-level impact: access, emissions, capacity, resilience, and interface quality.",
        "Use scenario testing before adding new infrastructure: improve the connection before expanding the component.",
    ]

    for interface in weakest_interfaces:
        recommendations.append(f"Reduce friction at {interface.connection}: {interface.issue}.")

    for opportunity in opportunities:
        recommendations.append(f"Explore opportunity: {opportunity}.")

    return recommendations


def run_scenario(profile: Dict, scenario: Dict[str, float]) -> Dict[str, int]:
    """Apply simple scenario levers to scores.

    Prototype logic: sliders change interface friction, car pressure, active mobility,
    and transit priority. Later phases can replace this with real transport models.
    """
    base_scores = {score.category: score.score for score in score_city_profile(profile)}

    transit_priority = scenario.get("transit_priority", 0)
    active_mobility = scenario.get("active_mobility", 0)
    interface_investment = scenario.get("interface_investment", 0)
    car_pressure = scenario.get("car_pressure", 0)

    adjusted = {
        "Mode Portfolio": base_scores.get("Mode Portfolio", 50) + transit_priority * 0.10 + active_mobility * 0.06,
        "Interface Quality": base_scores.get("Interface Quality", 50) + interface_investment * 0.25 + active_mobility * 0.08,
        "System Coordination": base_scores.get("System Coordination", 50) + interface_investment * 0.16 + transit_priority * 0.10 - car_pressure * 0.10,
        "System Resilience": base_scores.get("System Resilience", 50) + transit_priority * 0.08 + active_mobility * 0.10 - car_pressure * 0.05,
        "Accessibility": base_scores.get("Accessibility", 50) + active_mobility * 0.18 + interface_investment * 0.10 - car_pressure * 0.06,
    }

    return {key: clamp(value) for key, value in adjusted.items()}


def generate_dot_graph(profile: Dict) -> str:
    """Return a small Graphviz DOT graph for layer/interface visualization."""
    layers = profile.get("layers", {})
    interfaces = profile.get("interfaces", [])

    lines = [
        "digraph G {",
        "rankdir=LR;",
        "node [shape=box, style=rounded];",
    ]

    for layer, modes in layers.items():
        safe_layer = layer.replace("-", "_")
        lines.append(f'subgraph cluster_{safe_layer} {{ label="{layer.title()}";')
        for mode in modes[:8]:
            lines.append(f'"{mode}";')
        lines.append("}")

    for interface in interfaces:
        source = interface.get("from", "")
        target = interface.get("to", "")
        friction = interface.get("friction", 0.5)
        penwidth = 1 + friction * 4
        label = f"friction {friction:.2f}"
        lines.append(f'"{source}" -> "{target}" [label="{label}", penwidth={penwidth:.1f}];')

    lines.append("}")
    return "\n".join(lines)
