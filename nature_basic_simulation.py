import random as rnd
from pathlib import Path

import yaml

import consts
from alerts.eatalert import EatingAlert
from alerts.eventmanager import EventManager
from alerts.extinctalert import ExtinctAlert
from alerts.plantalert import PlantAlert
from entities.apexpredator import ApexPredator
from entities.block import Rock as Rock
from entities.block import Tree as Tree
from entities.herb import Herb as Herb
from entities.plant import Plant
from entities.predator import Pred as Pred
from grid import Grid as Grid


def print_world(world: Grid, turn: object) -> None:  # Chatgpt func fully
    """
    just prints the current state of the simulation grid.

    Args:
        world: grid object, the simulation grid containing all entities
        turn: int, the current turn number of the simulation.

    Returns: nothing

    """
    symbols = {
        Plant: "P",
        Herb: "H",
        Pred: "D",
        Rock: "R",
        Tree: "T",
        ApexPredator: "A",
    }
    print(f"\nTurn {turn} (P=plant, H=herbivore, D=predator, R=rock, T=tree):")
    for row in world.grid:
        print(" ".join(symbols.get(type(cell), ".") for cell in row))


def livingentities(world: Grid) -> list:
    return [cell for row in world.grid for cell in row if cell is not None]

def require_integer(values: dict, key: str, minimum: int) -> int:
    """Validate an integer configuration parameter.

    Args:
        values: Dictionary containing configuration values.
        key: Name of the parameter to validate.
        minimum: Minimum allowed value.

    Returns:
        The validated integer value.

    Raises:
        ValueError: If the value is missing, not an integer,
            or below the minimum.
    """
    value = values.get(key)

    if type(value) is not int or value < minimum:
        raise ValueError(
            f"{key} must be an integer greater than or equal to {minimum}"
        )

    return value
def validate_config(config: dict) -> None:
    """Validate simulation configuration before initialization.

    Args:
        config: Configuration loaded from YAML.

    Raises:
        ValueError: If required sections or parameters are invalid.
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")

    for section in ("grid", "parameters"):
        if not isinstance(config.get(section), dict):
            raise ValueError(f"Missing or invalid section: {section}")

    grid = config["grid"]
    parameters = config["parameters"]

    require_integer(grid, "width", 1)
    require_integer(grid, "height", 1)

    positive_parameters = (
        "T_PLANT",
        "T_HERBIVORE",
        "T_PREDATOR",
        "T_APEX_PREDATOR",
    )

    nonnegative_parameters = (
        "TURNS",
        "R_HERBIVORE_SIGHT",
        "R_PREDATOR_SIGHT",
        "R_APEX_PREDATOR_SIGHT",
        "T_COOLDOWN",
        "PLANT_SPAWN_EVERY",
    )

    for key in positive_parameters:
        require_integer(parameters, key, 1)

    for key in nonnegative_parameters:
        require_integer(parameters, key, 0)

    if not isinstance(config.get("entities"), list):
        raise ValueError("entities must be a list")

    valid_entity_types = {
        "Plant",
        "Herb",
        "Pred",
        "Rock",
        "Tree",
        "ApexPredator",
    }

    occupied_positions = set()

    for index, entity in enumerate(config["entities"]):
        if not isinstance(entity, dict):
            raise ValueError(f"Entity {index} must be a dictionary")

        entity_type = entity.get("type")

        if entity_type not in valid_entity_types:
            raise ValueError(
                f"Entity {index} has invalid type: {entity_type}"
            )

        x = require_integer(entity, "x", 0)
        y = require_integer(entity, "y", 0)

        if x >= grid["height"] or y >= grid["width"]:
            raise ValueError(
                f"Entity {index} has out-of-bounds coordinates: ({x}, {y})"
            )

        if (x, y) in occupied_positions:
            raise ValueError(
                f"Duplicate entity position: ({x}, {y})"
            )

        occupied_positions.add((x, y))
def run() -> None:
    """
    runs the simulation using conf from yaml.
    """
    rnd.seed(consts.DEFAULT_RANDOM_SEED)
    configpath = Path(__file__).resolve().parent / "config.yaml"
    try:
        with configpath.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise ValueError(f"Configuration file not found: {configpath}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML syntax: {exc}") from exc

    validate_config(config)

    gridconf = config["grid"]
    world = Grid(gridconf["width"], gridconf["height"])
    parameters = config["parameters"]

    TURNS = parameters["TURNS"]
    T_PLANT = parameters["T_PLANT"]
    PLANT_SPAWN_EVERY = parameters["PLANT_SPAWN_EVERY"]

    # maps entity names to  classes
    entity_classes = {
        "Plant": Plant,
        "Herb": Herb,
        "Pred": Pred,
        "Rock": Rock,
        "Tree": Tree,
        "ApexPredator": ApexPredator,
    }

    # maps entities that need a lifetime to their yaml parameter
    lifetimekeys = {
        "Plant": "T_PLANT",
        "Herb": "T_HERBIVORE",
        "Pred": "T_PREDATOR",
        "ApexPredator": "T_APEX_PREDATOR",
    }

    # create the initial entities
    for item in config["entities"]:
        entity_type = item["type"]
        x = item["x"]
        y = item["y"]

        if entity_type not in entity_classes:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entity_class = entity_classes[entity_type]

        if entity_type in lifetimekeys:
            steps = parameters[lifetimekeys[entity_type]]
            entity = entity_class(steps, x, y)
        else:
            entity = entity_class(x, y)

        world.addentity(entity)
    eventmanager = EventManager()
    world.eventmanager = eventmanager
    extinctalert = ExtinctAlert(livingentities(world))
    eventmanager.addObserver(extinctalert)
    eatingalert = EatingAlert()
    eventmanager.addObserver(eatingalert)
    plantalert = PlantAlert(world)
    eventmanager.addObserver(plantalert)
    print_world(world, 0)
    print("Starting entities:", len(livingentities(world)))

    for turn in range(1, TURNS + 1):
        for entity in livingentities(world):
            if world.grid[entity.x][entity.y] is not entity:
                continue

            entity.update(world, parameters)

        # spawn plants periodically
        if PLANT_SPAWN_EVERY and turn % PLANT_SPAWN_EVERY == 0:
            Plant(T_PLANT, 0, 0).spawn(world,T_PLANT)
        eventmanager.notifyObservers({
            "type": "turn_finished",
            "entities": livingentities(world)
        })
        print_world(world, turn)


if __name__ == "__main__":
    run()
