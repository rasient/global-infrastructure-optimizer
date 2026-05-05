# Design Notes

## Core Model

The project treats infrastructure as a flow system.

Transport is modeled across four layers:

1. Global
2. Regional
3. Urban
4. Micro / last-mile

Each layer contains modes. Each mode has performance dimensions. Interfaces connect modes and create friction.

## Key Objects

### Mode

A mode is a transport option such as metro, tram, bus, bicycle, walking, freight rail, or maritime shipping.

### Interface

An interface is a connection between two modes or layers.

Examples:

- metro → bicycle
- tram → walking
- regional rail → metro
- car → transit

Interfaces matter because many infrastructure failures happen between components, not inside components.

### Scenario

A scenario changes system levers:

- transit priority
- active mobility investment
- interface investment
- car pressure

The current scenario engine is intentionally simple and heuristic.
