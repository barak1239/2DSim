"""Small reproduction test for the ecosystem classes; no YAML needed."""
import random as rnd

PARAMETERS = {"R_HERBIVORE_SIGHT": 4, "R_PREDATOR_SIGHT": 4, "T_HERBIVORE": 12, "T_PREDATOR": 6, "T_COOLDOWN": 5}


# Change this import if your classes are saved in another Python file.
from entities.herb import Herb
from entities.plant import Plant
from grid import Grid


def print_world(world):
    symbols = {Herb: "H", Plant: "P"}
    for row in world.grid:
        print(" ".join(symbols.get(type(cell), ".") if cell is not None else "." for cell in row))
    print()


def herbivores(world):
    return [cell for row in world.grid for cell in row if isinstance(cell, Herb)]


def main():
    rnd.seed(7)  # Makes the baby's random position reproducible.
    world = Grid(7, 7)

    moving_herb = Herb(10, 2, 2)
    other_herb = Herb(10, 3, 2)
    plant = Plant(10, 4, 2)

    for entity in (moving_herb, other_herb, plant):
        world.addentity(entity)

    print("Before the turn (H = herbivore, P = plant, . = empty):")
    print_world(world)
    print("Herbivores:", len(herbivores(world)))

    # BFS should attempt to enter (3, 2), which contains the other herbivore.
    # Reproduction should create a baby instead of moving into that cell.
    moving_herb.update(world, PARAMETERS)

    print("After one turn:")
    print_world(world)
    print("Herbivores:", len(herbivores(world)))
    print("First parent's position:", (moving_herb.x, moving_herb.y))
    print("Second parent's position:", (other_herb.x, other_herb.y))
    print("Cooldowns:", moving_herb.cooldown, other_herb.cooldown)
    print("First parent's remaining steps:", moving_herb.steps)

    assert len(herbivores(world)) == 3, "Expected exactly one baby herbivore"
    assert (moving_herb.x, moving_herb.y) == (2, 2)
    assert (other_herb.x, other_herb.y) == (3, 2)
    assert moving_herb.cooldown == 5 and other_herb.cooldown == 5
    print("PASS: A baby was born; both parents stayed in place and got cooldowns.")


if __name__ == "__main__":
    main()
