from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TransportMode:
    name: str
    layer: str
    category: str
    capacity: int
    speed: int
    flexibility: int
    infrastructure_cost: int
    emissions_score: int
    accessibility: int
    resilience: int
    notes: str


TRANSPORT_LAYERS: Dict[str, List[TransportMode]] = {
    "global": [
        TransportMode("air", "global", "long-distance", 75, 100, 65, 90, 25, 55, 70, "Fast long-distance passenger and cargo movement, high cost and emissions."),
        TransportMode("maritime", "global", "freight", 100, 35, 35, 85, 65, 30, 75, "Very high-capacity global freight through ports and shipping lanes."),
        TransportMode("high-speed rail", "global", "intercity", 85, 90, 45, 95, 90, 75, 80, "High-capacity regional/global corridor mobility where density supports it."),
        TransportMode("freight rail", "global", "freight", 95, 55, 40, 80, 85, 35, 85, "Efficient high-volume freight backbone."),
        TransportMode("highway", "global", "road", 70, 75, 90, 70, 45, 60, 70, "Flexible long-distance road network for cars, coaches, vans, and freight."),
        TransportMode("pipeline", "global", "resource-flow", 100, 45, 15, 90, 80, 10, 90, "Continuous fixed-route movement of oil, gas, water, or other resources."),
    ],
    "regional": [
        TransportMode("intercity rail", "regional", "rail", 85, 80, 45, 80, 90, 75, 85, "City-to-city rail backbone."),
        TransportMode("regional rail", "regional", "rail", 80, 70, 55, 75, 90, 80, 85, "Commuter and regional access into urban cores."),
        TransportMode("coach bus", "regional", "bus", 55, 65, 80, 45, 65, 65, 70, "Flexible lower-cost regional service."),
        TransportMode("motorway", "regional", "road", 70, 80, 90, 70, 45, 60, 70, "Regional car and freight corridors."),
        TransportMode("ferry", "regional", "water", 60, 45, 45, 60, 70, 55, 65, "Useful where geography creates water-crossing constraints."),
        TransportMode("suburban rail", "regional", "rail", 80, 70, 55, 75, 90, 80, 80, "Outer-area connection into dense city networks."),
    ],
    "urban": [
        TransportMode("metro", "urban", "rapid-transit", 100, 85, 35, 100, 95, 85, 90, "Highest urban capacity, high fixed infrastructure cost."),
        TransportMode("tram", "urban", "surface-rail", 75, 55, 55, 70, 90, 90, 80, "Strong visible surface transit with good stop access."),
        TransportMode("light rail", "urban", "surface-rail", 80, 65, 50, 75, 90, 85, 82, "Medium/high capacity rail between tram and metro."),
        TransportMode("small tram", "urban", "micro-rail", 45, 45, 70, 55, 88, 90, 78, "Clayton-style gap-filler: lower capacity and lower cost than full tram, stronger than shuttle/bus in selected streets."),
        TransportMode("bus", "urban", "road-transit", 55, 45, 90, 35, 60, 85, 75, "Flexible public transport coverage layer."),
        TransportMode("trolleybus", "urban", "electric-road-transit", 55, 45, 70, 55, 90, 85, 78, "Electric bus-like mode with fixed overhead infrastructure."),
        TransportMode("car", "urban", "private-road", 35, 60, 95, 65, 30, 45, 55, "Flexible but space-intensive and congestion-sensitive."),
        TransportMode("taxi", "urban", "on-demand", 25, 55, 90, 30, 35, 55, 50, "Flexible door-to-door service with limited capacity."),
        TransportMode("ride-hailing", "urban", "on-demand", 25, 55, 90, 30, 35, 55, 50, "App-based on-demand mobility; can increase vehicle-km if unmanaged."),
        TransportMode("delivery van", "urban", "urban-logistics", 35, 50, 85, 45, 35, 35, 60, "Last-mile goods movement; curb space and congestion impact matter."),
        TransportMode("minibus taxi", "urban", "informal-transit", 45, 50, 95, 30, 45, 70, 65, "Flexible semi-formal/informal urban transport layer."),
    ],
    "micro": [
        TransportMode("walking", "micro", "active", 20, 15, 100, 20, 100, 100, 85, "Foundation of every trip and every transfer."),
        TransportMode("bicycle", "micro", "active", 25, 35, 95, 30, 100, 80, 80, "Low-cost, low-emission mobility where safe networks exist."),
        TransportMode("e-bike", "micro", "active-electric", 30, 45, 95, 35, 95, 75, 80, "Extends cycling range and reduces hill/distance friction."),
        TransportMode("e-scooter", "micro", "micromobility", 15, 35, 90, 25, 90, 65, 60, "Flexible short-distance first/last-mile option."),
        TransportMode("cargo bike", "micro", "micro-logistics", 25, 30, 80, 30, 100, 65, 75, "Urban logistics alternative for dense areas."),
        TransportMode("wheelchair access", "micro", "accessibility", 15, 15, 70, 45, 100, 100, 90, "Accessibility layer: curb cuts, elevators, surface quality, and barrier-free transfers."),
    ],
}


def flatten_modes() -> List[TransportMode]:
    return [mode for modes in TRANSPORT_LAYERS.values() for mode in modes]


def modes_by_name() -> Dict[str, TransportMode]:
    return {mode.name: mode for mode in flatten_modes()}


def detect_profile_layers(profile: Dict) -> Dict[str, List[str]]:
    present_modes = set(profile.get("dominant_modes", [])) | set(profile.get("additional_modes", []))
    result: Dict[str, List[str]] = {}
    for layer, modes in TRANSPORT_LAYERS.items():
        names = [m.name for m in modes if m.name in present_modes]
        result[layer] = names
    return result


def layer_completeness(profile: Dict) -> Dict[str, int]:
    detected = detect_profile_layers(profile)
    return {
        layer: int(round(100 * len(names) / max(1, len(TRANSPORT_LAYERS[layer]))))
        for layer, names in detected.items()
    }


def build_mode_table(profile: Dict) -> List[Dict]:
    present = set(profile.get("dominant_modes", [])) | set(profile.get("additional_modes", []))
    rows = []
    for mode in flatten_modes():
        rows.append({
            "mode": mode.name,
            "layer": mode.layer,
            "category": mode.category,
            "in_profile": mode.name in present,
            "capacity": mode.capacity,
            "speed": mode.speed,
            "flexibility": mode.flexibility,
            "infrastructure_cost": mode.infrastructure_cost,
            "emissions_score": mode.emissions_score,
            "accessibility": mode.accessibility,
            "resilience": mode.resilience,
            "notes": mode.notes,
        })
    return rows
