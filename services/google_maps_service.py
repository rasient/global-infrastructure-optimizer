from __future__ import annotations

import os
from typing import Dict, Any

import requests


class GoogleMapsService:
    """Small placeholder for future Google Maps integration.

    MVP uses mock mode. Later this service can call:
    - Geocoding API
    - Routes API
    - Route Matrix API
    - Places API
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.mock_mode = os.getenv("USE_MOCK_MODE", "true").lower() == "true"

    def geocode_city(self, city: str) -> Dict[str, Any]:
        if self.mock_mode or not self.api_key:
            return {
                "city": city,
                "lat": 47.4979 if city.lower() == "budapest" else 48.2082,
                "lng": 19.0402 if city.lower() == "budapest" else 16.3738,
                "source": "mock",
            }

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": city, "key": self.api_key}
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def route_summary(self, origin: str, destination: str, mode: str = "transit") -> Dict[str, Any]:
        if self.mock_mode or not self.api_key:
            return {
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "duration_minutes": 28 if mode == "transit" else 22,
                "distance_km": 6.4,
                "source": "mock",
            }

        # Placeholder: use Google Routes API in a later version.
        raise NotImplementedError("Real Routes API integration is planned in the roadmap.")
