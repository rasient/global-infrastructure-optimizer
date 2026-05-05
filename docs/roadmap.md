# Roadmap

## Phase 1 — Foundation ✅

- define global / regional / urban / micro transport layers
- expand the mode portfolio with metro, tram, small tram, trolleybus, bicycle, walking, and accessibility
- keep sample city profiles easy to edit
- preserve mock mode so the app runs without API keys

## Phase 2 — System Modeling ✅

- add mode-level scoring
- add interface friction scoring
- model transfers between transport modes
- identify bottlenecks and weak interfaces
- create a simple scenario engine

## Phase 3 — Visualization ✅

- show layer tables
- show mode portfolio tables
- show interface friction tables
- add Graphviz system map for layer/interface visualization
- compare baseline vs scenario scores

## Phase 4 — Interactive Tool ✅

- Streamlit dashboard
- city selector
- scenario sliders
- score comparison
- diagnosis tab
- exportable Markdown report

## Phase 5 — Real Data Ready 🟡

Prototype support exists, but real data still needs to be connected.

Planned integrations:

- Google Maps Geocoding API
- Google Routes API
- transit travel time comparison
- city-level open data
- GTFS feeds
- emissions factors
- accessibility datasets

## Phase 6 — Expansion 🟡

The architecture can be extended beyond transport.

Potential next systems:

- energy grids
- water systems
- logistics networks
- healthcare access
- emergency response
- digital infrastructure

## Long-Term Vision

A decision-support prototype for understanding infrastructure as interacting layers, not isolated assets.

The goal is not to replace planners.

The goal is to make system behavior, bottlenecks, interfaces, and trade-offs easier to see.
