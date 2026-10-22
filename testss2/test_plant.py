"""Small tests for Plant using the user's existing simulation classes.

Place this next to the file that defines Grid, Plant, and Herb.
Change the import below if that file has a different name.
"""

import random
from entities.entity import Grid, Plant, Herb


def plants_in(world):
    return [cell for row in world.grid for cell in row if isinstance(cell, Plant)]


def test_lifespan():
    world = Grid(5, 5)
    plant = Plant(2, 2, 3)
    world.addentity(plant)
    plant.update(world)
    assert plant.steps == 1
    assert world.grid[2][3] is plant
    plant.update(world)
    assert world.grid[2][3] is None
    print("Plant lifespan: PASS (dies after 2 updates)")


def test_random_spawn():
    random.seed(42)  # Makes the random test repeatable
    world = Grid(5, 5)
    parent = Plant(4, 2, 2)
    world.addentity(parent)
    parent.spawn(world)
    plants = plants_in(world)
    assert len(plants) == 2, f"Expected 2 plants, got {len(plants)}"
    assert world.grid[2][2] is parent, "Spawning replaced the parent"
    baby = next(p for p in plants if p is not parent)
    assert (baby.x, baby.y) != (parent.x, parent.y)
    assert baby.steps == parent.steps
    assert world.grid[baby.x][baby.y] is baby
    print(f"Random spawning: PASS (new plant at {(baby.x, baby.y)})")


def test_stays_still():
    world = Grid(5, 5)
    plant = Plant(3, 1, 4)
    world.addentity(plant)
    initial_position = (plant.x, plant.y)
    plant.update(world)
    assert (plant.x, plant.y) == initial_position
    assert world.grid[1][4] is plant
    print("Plant stationary: PASS (position unchanged)")


def test_eaten():
    world = Grid(5, 5)
    herbivore = Herb(6, 2, 1)
    plant = Plant(4, 2, 2)
    world.addentity(herbivore)
    world.addentity(plant)
    herbivore.update(world, 2, 5, T_HERBIVORE=3)
    assert world.grid[2][2] is herbivore, "Herbivore did not reach plant"
    assert all(cell is not plant for row in world.grid for cell in row), (
        "Plant still on grid"
    )
    assert herbivore.steps == 9, f"Expected 6 + 4 - 1 = 9 steps, got {herbivore.steps}"
    print("Plant consumed: PASS (plant removed; herbivore steps = 9)")


if __name__ == "__main__":
    test_lifespan()
    test_random_spawn()
    test_stays_still()
    test_eaten()
    print("ALL PLANT TESTS PASSED")
