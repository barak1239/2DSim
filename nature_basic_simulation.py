from typing import List

import yaml
import random
import entities
import grid
from entities.plant import Plant
from entities.mobileentity import Pred as Pred, Herb as Herb
from grid import Grid as Grid
from entities.block import Rock as Rock, Tree as Tree
from entities.apexpredator import ApexPredator


def print_world(world, turn) -> None:  # Chatgpt func fully
    """
    just print the world
    Args:
        world: grid
        turn: int

    Returns:

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


def livingentities(world) -> list:
    return [cell for row in world.grid for cell in row if cell is not None]


def run() -> None:
    """
    runs the simulation using conf from yaml.
    """
    random.seed(42)

    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

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

    print_world(world, 0)
    print("Starting entities:", len(livingentities(world)))

    for turn in range(1, TURNS + 1):
        for entity in livingentities(world):
            if world.grid[entity.x][entity.y] is not entity:
                continue

            entity.update(world, parameters)

        # spawn plants periodically
        if PLANT_SPAWN_EVERY and turn % PLANT_SPAWN_EVERY == 0:
            if any(cell is None for row in world.grid for cell in row):
                Plant(T_PLANT, 0, 0).spawn(world)

        print_world(world, turn)


if __name__ == "__main__":
    run()
