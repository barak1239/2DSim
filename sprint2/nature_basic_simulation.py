import yaml
import random
from plant import Plant
from mobileentity import Pred as Pred, Herb as Herb
from grid import Grid as Grid
from sprint2.block import Rock as Rock, Tree as Tree

def print_world(world, turn): #Chatgpt func fully
    symbols = {Plant: "P", Herb: "H", Pred: "D", Rock: "R", Tree: "T"}
    print(f"\nTurn {turn} (P=plant, H=herbivore, D=predator, R=rock, T=tree):")
    for row in world.grid:
        print(" ".join(symbols.get(type(cell), ".") for cell in row))


def living_entities(world):
    return [cell for row in world.grid for cell in row if cell is not None]


def run():
    random.seed(42)
    with open("./config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    gridconf = config["grid"]
    world = Grid(gridconf["width"], gridconf["height"])
    parameters = config["parameters"]
    TURNS = parameters["TURNS"]
    T_PLANT = parameters["T_PLANT"]
    T_HERBIVORE = parameters["T_HERBIVORE"]
    T_PREDATOR = parameters["T_PREDATOR"]
    R_HERBIVORE_SIGHT = parameters["R_HERBIVORE_SIGHT"]
    R_PREDATOR_SIGHT = parameters["R_PREDATOR_SIGHT"]
    T_COOLDOWN = parameters["T_COOLDOWN"]
    PLANT_SPAWN_EVERY = parameters["PLANT_SPAWN_EVERY"]
    for item in config["entities"]:
        entity_type = item["type"]
        x = item["x"]
        y = item["y"]

        if entity_type == "Plant":
            entity = Plant(T_PLANT, x, y)
        elif entity_type == "Herb":
            entity = Herb(T_HERBIVORE, x, y)
        elif entity_type == "Pred":
            entity = Pred(T_PREDATOR, x, y)
        elif entity_type == "Rock":
            entity = Rock(x, y)
        elif entity_type == "Tree":
            entity = Tree(x, y)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
        world.addentity(entity)
    print_world(world, 0)
    print("Starting entities:", len(living_entities(world)))
    for turn in range(1, TURNS + 1):
        #newborns wont act until the next turn.
        for entity in living_entities(world):
            if world.grid[entity.x][entity.y] is not entity:
                continue
            if isinstance(entity, Herb):
                entity.update(world, R_HERBIVORE_SIGHT, T_COOLDOWN,T_HERBIVORE)
            elif isinstance(entity, Pred):
                entity.update(world, R_PREDATOR_SIGHT, T_COOLDOWN,T_HERBIVORE)
            elif isinstance(entity, Plant):
                entity.update(world)
            # rocks trees are still objects
        if PLANT_SPAWN_EVERY and turn % PLANT_SPAWN_EVERY == 0:
            if any(cell is None for row in world.grid for cell in row):
                Plant(T_PLANT, 0, 0).spawn(world)

        print_world(world, turn)


if __name__ == "__main__":
    run()
