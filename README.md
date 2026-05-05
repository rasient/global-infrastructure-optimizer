## 🧠 Part of Systems Lab

This project is part of a broader exploration:

→ understanding how systems behave when treated as interconnected

Main repo:
https://github.com/rasient/systems-lab

# Global Infrastructure Optimizer

A prototype decision-support tool for analyzing multimodal transport infrastructure using map data and AI-assisted systems thinking.

This project connects a simple idea:

> Transport is not one system. It is a portfolio of systems.

The goal is to help analyze how different transport modes work together in a city or region, identify weak interfaces, and generate practical infrastructure improvement ideas.

---

## What this app does

The prototype lets you:

- select a sample city profile
- compare transport modes
- analyze infrastructure gaps
- score multimodal coordination
- evaluate interface friction
- test simple scenarios with sliders
- visualize transport layers and interfaces
- generate AI-style recommendations using mock logic first
- export a Markdown report
- later connect Google Maps and OpenAI APIs

---

## Why this exists

Most transport debates focus on single modes:

- cars
- buses
- rail
- cycling
- walking

But real mobility performance depends on how these modes interact.

The important questions are:

- Where do transfers fail?
- Which areas are overdependent on cars?
- Where are multimodal connections weak?
- What infrastructure would improve the whole system, not just one mode?
- Which interface creates the most friction?
- What happens when car pressure increases or transit priority improves?

---

## Multi-Layer Transport Model

The transport system is modeled as four connected layers.

### 🌍 Global

Long-distance movement of people, goods, energy, and resources.

Examples:

- air
- maritime
- freight rail
- high-speed rail
- highways
- pipelines

### 🌐 Regional

Movement between cities, regions, and economic zones.

Examples:

- intercity rail
- regional rail
- coach buses
- motorways
- ferries
- logistics corridors

### 🏙️ Urban

Movement inside cities and metropolitan areas.

Examples:

- metro
- tram
- light rail
- small tram
- trolleybus
- bus
- suburban rail
- car
- taxi
- ride-hailing
- delivery van

### 🚶 Micro / Last-Mile

The access layer that determines whether the rest of the system actually works.

Examples:

- walking
- bicycle
- e-bike
- scooter
- cargo bike
- wheelchair access
- sidewalks
- crossings
- bike lanes

---

## Why Interfaces Matter

A strong transport mode can still fail in a weak system.

Examples:

- good metro + poor walking access → low usability
- bike network without transit connection → limited reach
- regional rail without coordination → slow transfers
- buses in car traffic → unreliable service
- tram stops without safe crossings → weak accessibility

The problem is not only the mode.

The problem is often the connection.

---

## MVP Features

- Streamlit dashboard
- sample city profiles
- multi-layer transport model
- transport mode scoring
- interface friction scoring
- scenario sliders
- baseline vs scenario comparison
- Graphviz system map
- infrastructure gap analysis
- recommendation generator
- exportable Markdown report
- placeholder services for Google Maps and OpenAI

---

## Project Structure

```text
global-infrastructure-optimizer/
│
├── app/
│   └── main.py
│
├── data/
│   └── sample_city_profiles.json
│
├── services/
│   ├── google_maps_service.py
│   ├── openai_service.py
│   └── scoring_service.py
│
├── prompts/
│   └── infrastructure_analysis.md
│
├── outputs/
│   └── .gitkeep
│
├── docs/
│   ├── design.md
│   └── roadmap.md
│
├── examples/
│   └── sample_scenarios.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
source venv/Scripts/activate

# macOS / Linux
source venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create environment file

```bash
cp .env.example .env
```

You can run the prototype without API keys using mock mode.

Later, add:

```text
OPENAI_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here
USE_MOCK_MODE=true
```

---

### 4. Run the app

```bash
python -m streamlit run app/main.py
```

---

## Example Use Case

1. Select Budapest as a sample city
2. Review the multi-layer transport model
3. Compare mode scores
4. Identify high-friction interfaces
5. Adjust scenario sliders
6. Compare baseline vs scenario results
7. Generate a system-level diagnosis
8. Export a Markdown report

---

## Small Tram Concept

The project includes a small tram as a missing-middle urban mobility layer.

It sits between:

- bus
- tram
- metro

Potential role:

- cheaper than full tram infrastructure
- more structured than buses
- useful for medium-density corridors
- possible feeder to metro or regional rail
- useful where streets are constrained but demand is higher than bus capacity

In systems terms, the small tram is not just a vehicle.

It is a design intervention for filling gaps in the urban mobility spectrum.

---

## Docs

Additional documentation:

- [Design Notes](docs/design.md)
- [Roadmap](docs/roadmap.md)
- [Sample Scenarios](examples/sample_scenarios.md)

---

## Roadmap Status

Current prototype status:

- Phase 1 — Foundation: done
- Phase 2 — System Modeling: done at prototype level
- Phase 3 — Visualization: done at prototype level
- Phase 4 — Interactive Tool: done at prototype level
- Phase 5 — Real Data Ready: prepared, not fully connected
- Phase 6 — Expansion: architecture prepared

See [docs/roadmap.md](docs/roadmap.md) for details.

---

## Core Message

We don’t have infrastructure problems.

We have system design problems.

A city does not fail because it lacks one perfect transport mode.

It fails when modes do not connect, incentives do not align, and the system makes good choices difficult.

---

## Author

Alexander Berg

GitHub:
https://github.com/rasient
