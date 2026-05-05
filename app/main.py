from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.google_maps_service import GoogleMapsService
from services.openai_service import OpenAIAnalysisService
from services.scoring_service import (
    generate_dot_graph,
    generate_recommendations,
    identify_system_gaps,
    mode_portfolio_table,
    run_scenario,
    score_city_profile,
    score_interfaces,
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
    st.caption("Multi-layer infrastructure prototype: global → regional → urban → micro.")

    profiles = load_profiles()
    city_names = [f"{p['city']}, {p['country']}" for p in profiles]

    selected = st.sidebar.selectbox("Select city profile", city_names)
    profile = profiles[city_names.index(selected)]

    maps_service = GoogleMapsService()
    ai_service = OpenAIAnalysisService()

    st.sidebar.header("Scenario levers")
    scenario = {
        "transit_priority": st.sidebar.slider("Transit priority", 0, 100, 50),
        "active_mobility": st.sidebar.slider("Walking / cycling investment", 0, 100, 50),
        "interface_investment": st.sidebar.slider("Transfer / interface investment", 0, 100, 50),
        "car_pressure": st.sidebar.slider("Car pressure", 0, 100, 50),
    }

    profile_col, score_col = st.columns([1, 1])

    with profile_col:
        st.subheader("City Profile")
        st.write(f"**City:** {profile['city']}")
        st.write(f"**Country:** {profile['country']}")
        st.write(f"**Density:** {profile['density']}")
        st.write("**Dominant modes:**")
        st.write(", ".join(profile["dominant_modes"]))

        geocode = maps_service.geocode_city(profile["city"])
        st.write("**Map reference:**")
        st.json(geocode)

    with score_col:
        st.subheader("System Scores")
        scores = score_city_profile(profile)
        score_df = pd.DataFrame([s.__dict__ for s in scores])
        st.dataframe(score_df, use_container_width=True, hide_index=True)

        for score in scores:
            st.progress(score.score / 100, text=f"{score.category}: {score.score}/100")

    st.divider()

    layer_tab, interface_tab, scenario_tab, diagnosis_tab = st.tabs(
        ["Layers", "Interfaces", "Scenario", "Diagnosis"]
    )

    with layer_tab:
        st.subheader("Multi-Layer Transport Model")
        layer_rows = []
        for layer, modes in profile.get("layers", {}).items():
            layer_rows.append({"layer": layer, "modes": ", ".join(modes)})
        st.dataframe(pd.DataFrame(layer_rows), use_container_width=True, hide_index=True)

        st.subheader("Mode Portfolio")
        mode_rows = mode_portfolio_table(profile)
        if mode_rows:
            st.dataframe(pd.DataFrame(mode_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No mode-level scores defined for this profile yet.")

        st.subheader("System Map")
        st.graphviz_chart(generate_dot_graph(profile), use_container_width=True)

    with interface_tab:
        st.subheader("Interface Friction")
        interface_scores = score_interfaces(profile)
        if interface_scores:
            interface_df = pd.DataFrame([s.__dict__ for s in interface_scores])
            st.dataframe(interface_df, use_container_width=True, hide_index=True)
            st.caption("Lower friction means a smoother transfer or connection between modes.")
        else:
            st.info("No interfaces defined for this profile yet.")

    with scenario_tab:
        st.subheader("Scenario Comparison")
        base = {score.category: score.score for score in score_city_profile(profile)}
        adjusted = run_scenario(profile, scenario)
        comparison = pd.DataFrame(
            [
                {"metric": metric, "baseline": base.get(metric, 0), "scenario": adjusted.get(metric, 0), "delta": adjusted.get(metric, 0) - base.get(metric, 0)}
                for metric in adjusted
            ]
        )
        st.dataframe(comparison, use_container_width=True, hide_index=True)
        st.bar_chart(comparison.set_index("metric")[["baseline", "scenario"]])

    with diagnosis_tab:
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
        "Prototype mode: mock data first, real APIs later. Designed for systems thinking, not production planning."
    )


if __name__ == "__main__":
    main()
