from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.google_maps_service import GoogleMapsService
from services.openai_service import OpenAIAnalysisService
from services.scoring_service import (
    generate_recommendations,
    identify_system_gaps,
    score_city_profile,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_city_profiles.json"
OUTPUT_DIR = ROOT / "outputs"


def load_profiles():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_report(city: str, report: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    safe_city = city.lower().replace(" ", "-")
    path = OUTPUT_DIR / f"{safe_city}-infrastructure-report.md"
    path.write_text(report, encoding="utf-8")
    return path


def main() -> None:
    load_dotenv(ROOT / ".env")

    st.set_page_config(
        page_title="Global Infrastructure Optimizer",
        page_icon="🚆",
        layout="wide",
    )

    st.title("🚆 Global Infrastructure Optimizer")
    st.caption("A prototype decision-support tool for multimodal transport systems.")

    profiles = load_profiles()
    city_names = [f"{p['city']}, {p['country']}" for p in profiles]

    selected = st.sidebar.selectbox("Select city profile", city_names)
    profile = profiles[city_names.index(selected)]

    maps_service = GoogleMapsService()
    ai_service = OpenAIAnalysisService()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("City Profile")
        st.write(f"**City:** {profile['city']}")
        st.write(f"**Country:** {profile['country']}")
        st.write(f"**Density:** {profile['density']}")
        st.write("**Dominant modes:**")
        st.write(", ".join(profile["dominant_modes"]))

        geocode = maps_service.geocode_city(profile["city"])
        st.write("**Map reference:**")
        st.json(geocode)

    with col2:
        st.subheader("System Scores")
        scores = score_city_profile(profile)
        score_df = pd.DataFrame([s.__dict__ for s in scores])
        st.dataframe(score_df, use_container_width=True, hide_index=True)

        for score in scores:
            st.progress(score.score / 100, text=f"{score.category}: {score.score}/100")

    st.divider()

    gaps = identify_system_gaps(profile)
    recommendations = generate_recommendations(profile)

    gap_col, rec_col = st.columns(2)

    with gap_col:
        st.subheader("Detected System Gaps")
        for gap in gaps:
            st.write(f"- {gap}")

    with rec_col:
        st.subheader("Recommended Interventions")
        for rec in recommendations:
            st.write(f"- {rec}")

    st.divider()

    st.subheader("AI-Style System Diagnosis")
    report = ai_service.analyze_profile(profile, gaps, recommendations)
    st.markdown(report)

    if st.button("Export Markdown Report"):
        path = save_report(profile["city"], report)
        st.success(f"Report saved to {path}")

    st.sidebar.divider()
    st.sidebar.info(
        "MVP runs in mock mode by default. Add API keys to .env later for real integrations."
    )


if __name__ == "__main__":
    main()
