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

The MVP lets you:

- select a sample city profile
- compare transport modes
- analyze infrastructure gaps
- score multimodal coordination
- generate AI-style recommendations using mock logic first
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

---

## MVP Features

- Streamlit dashboard
- sample city profiles
- transport mode scoring
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
│   └── roadmap.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Create project folder

Recommended location on Windows:

```bash
mkdir -p /c/projects
cd /c/projects
```

Extract this repo into:

```text
C:\projects\global-infrastructure-optimizer
```

---

### 2. Create virtual environment

```bash
cd /c/projects/global-infrastructure-optimizer
python -m venv venv
source venv/Scripts/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create environment file

```bash
cp .env.example .env
```

You can run the MVP without API keys using mock mode.

Later, add:

```text
OPENAI_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here
USE_MOCK_MODE=true
```

---

### 5. Run the app

```bash
python -m streamlit run app/main.py
```

---

## GitHub Setup

Create a new GitHub repository:

```text
Repository name:
global-infrastructure-optimizer

Description:
A prototype decision-support tool for analyzing multimodal transport infrastructure using Google Maps data and AI-assisted systems thinking.

Visibility:
Public or Private

Initialize with README:
NO

Add .gitignore:
NO

License:
None for now
```

Then run:

```bash
cd /c/projects/global-infrastructure-optimizer

git init
git add .
git commit -m "Initial commit: Global Infrastructure Optimizer"

git branch -M main
git remote add origin https://github.com/rasient/global-infrastructure-optimizer.git
git push -u origin main
```

If GitHub rejects the push because the remote already has files:

```bash
git push -u origin main --force
```

Only use force push if the remote repo does not contain anything important.

---

## Example Use Case

1. Select Budapest as sample city
2. Review current mode portfolio
3. Identify coordination problems
4. Generate system-level recommendations
5. Export report

---

## Future Improvements

See [`docs/roadmap.md`](docs/roadmap.md).

---

## Author

Alexander Berg  
GitHub: [rasient](https://github.com/rasient)

Focused on sociotechnical systems, AI-assisted analysis, infrastructure, and real-world system design.
