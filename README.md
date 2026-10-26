# 2DSim — Game of Life & Nature Simulation

## Overview

2DSim is a Python project containing two grid-based simulations:

- **Game of Life (Sprint 1):** A cellular automaton where cells survive, die, or reproduce based on their neighbors.
- **Nature Simulation (Sprints 2–3):** An ecosystem where plants, herbivores, predators, and apex predators interact on a configurable 2D grid.

## Nature Simulation

The nature simulation includes the following entities:

| Entity | Behavior |
|---|---|
| Plant | Has a limited lifetime and is periodically regenerated |
| Herb | Searches for plants, eats them to gain lifetime, and can reproduce |
| Pred | Hunts herbivores to gain lifetime |
| ApexPredator | Hunts both herbivores and predators |
| Rock | Blocks animal movement |
| Tree | Blocks animal movement |

Mobile entities use Breadth-First Search (BFS) to find reachable food within their sight range. When food is unavailable, they attempt random movement.

Herbivores reproduce when they encounter a compatible partner and have no reproduction cooldown.

The simulation also uses the Observer design pattern through `EventManager` to report:

- Predator feeding events
- Species extinction
- Plant coverage exceeding 90% of the grid

## Requirements

- Python 3.10 or newer (verify compatibility with your installed version)
- Dependencies from `requirements.txt`
- Tkinter and a graphical environment for the Sprint 1 Matplotlib animation when using the TkAgg backend

## Installation

Clone the repository:

```bash
git clone https://github.com/barak1239/2DSim.git
cd 2DSim
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Simulations

### Nature Simulation

From the project root:

```bash
python nature_basic_simulation.py
```

The program loads `config.yaml`, initializes the entities, and runs the simulation for the configured number of turns.

Each turn updates entity movement, feeding, reproduction, remaining lifetime, and event notifications.

### Game of Life

The Sprint 1 implementation is located in `sprint1/`.

Its `main.py` runs a Matplotlib animation of the grid.

The supported patterns include:

- `canoe.txt`
- `cloverleaf.txt`
- `hammerhead.txt`
- `checkedpattern1.txt`

Pattern files represent grid states using `0` for dead cells and `1` for living cells.

Ensure that the selected pattern file can be found relative to the working directory expected by the Sprint 1 code.

## Configuration

The nature simulation uses `config.yaml`.

Example:

```yaml
parameters:
  TURNS: 200
  T_PLANT: 16
  T_HERBIVORE: 12
  T_PREDATOR: 6
  T_APEX_PREDATOR: 8
  R_HERBIVORE_SIGHT: 3
  R_PREDATOR_SIGHT: 3
  R_APEX_PREDATOR_SIGHT: 4
  T_COOLDOWN: 5
  PLANT_SPAWN_EVERY: 1

grid:
  type: Grid
  width: 30
  height: 30

entities:
  - type: Plant
    x: 2
    y: 4
  - type: Herb
    x: 3
    y: 5
  - type: Pred
    x: 7
    y: 15
```

The configuration determines grid dimensions, starting entities, entity lifetimes, sight ranges, reproduction cooldown, and plant spawning frequency.

Configuration validation checks required values and rejects invalid entity coordinates or duplicate initial positions.

Coordinates are zero-based: `x` represents the row index and `y` represents the column index.

## Running Tests

Run the complete pytest suite from the project root:

```bash
python -m pytest -v
```

The tests cover entity movement, feeding, reproduction, cooldown behavior, lifespan expiration, pathfinding, and event notifications.

## Code Quality

Ruff is used for linting and formatting.

Check the project:

```bash
python -m ruff check .
```

Verify formatting:

```bash
python -m ruff format . --check
```

Automatically apply safe lint fixes:

```bash
python -m ruff check . --fix
```

## Project Structure

```text
2DSim/
├── sprint1/                  # Game of Life
├── entities/                 # Simulation entity classes
├── alerts/                   # EventManager and observers
├── testss2/                  # Simulation tests
├── nature_basic_simulation.py
├── config.yaml
├── consts.py
├── grid.py
├── requirements.txt
└── README.md
```

## Development

The project was developed across three sprints.

**Sprint 1:** Game of Life simulation, pattern loading, and animation.

**Sprint 2:** Nature simulation with plants, herbivores, predators, obstacles, movement, and reproduction.

**Sprint 3:** Refactored shared entity behavior, introduced apex predators and the Observer pattern, and extended automated testing.

*the improved readme was created using chatgpt :)