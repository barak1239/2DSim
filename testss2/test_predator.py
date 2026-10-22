"""Small, repeatable tests for the current predator logic (no YAML needed).

Place next to the Python file containing Grid, Pred, Herb, and Plant.
If necessary, change the import below to match your filename.
"""

import random as rnd
from entities.entity import Grid, Pred, Herb, Plant


def count_type(world, entity_type):
    return sum(isinstance(cell, entity_type) for row in world.grid for cell in row)


def test_hunting_and_refueling():
    world = Grid(7, 7)
    predator = Pred(6, 2, 2)
    herbivore = Herb(4, 2, 3)
    world.addentity(predator)
    world.addentity(herbivore)

    path = predator.look(3, world)
    assert path == [(2, 3)], f"Unexpected shortest path: {path}"

    predator.update(world, 3, 5, T_HERBIVORE=3)
    assert (predator.x, predator.y) == (2, 3), "Predator didn't reach the herbivore"
    assert world.grid[2][3] is predator, "Predator is missing from its new cell"
    assert world.grid[2][2] is None, "Predator's old cell wasn't cleared"
    assert count_type(world, Herb) == 0, "Herbivore wasn't eaten"
    assert predator.steps == 9, f"Expected lifespan 6 + 4 - 1 = 9; got {predator.steps}"
    print("Hunting and refueling: PASS (herbivore eaten; predator steps = 9)")


def test_plant_destroyed_without_refueling():
    world = Grid(7, 7)
    predator = Pred(6, 2, 2)
    plant = Plant(20, 2, 3)
    world.addentity(predator)
    world.addentity(plant)

    # Force one permitted step onto a plant to test the encounter directly;
    # a random wandering choice may or may not pick that particular cell.
    predator.move([(2, 3)], world, 5, T_HERBIVORE=3)

    assert (predator.x, predator.y) == (2, 3), "Predator didn't move onto the plant"
    assert world.grid[2][3] is predator, "Plant wasn't replaced by predator"
    assert count_type(world, Plant) == 0, "Plant was not destroyed"
    assert predator.steps == 6, "Destroying a plant should not refuel the predator"
    print("Stepping on plant: PASS (plant destroyed, no refueling)")


def test_lifespan_death():
    world = Grid(7, 7)
    predator = Pred(1, 2, 2)
    world.addentity(predator)
    rnd.seed(0)

    predator.update(world, 3, 5, T_HERBIVORE=3)

    assert predator.steps == 0, f"Expected steps = 0, got {predator.steps}"
    assert count_type(world, Pred) == 0, "Expired predator is still present on grid"
    print("Lifespan expiry: PASS (predator removed at zero steps)")


def test_closest_herbivore():
    world = Grid(7, 7)
    predator = Pred(10, 2, 2)
    close_herbivore = Herb(5, 2, 3)
    far_herbivore = Herb(5, 2, 5)
    for entity in (predator, close_herbivore, far_herbivore):
        world.addentity(entity)

    path = predator.look(5, world)
    assert path == [(2, 3)], f"Expected path toward nearest herbivore; got {path}"
    print("Nearest herbivore: PASS (BFS selects closest target)")


if __name__ == "__main__":
    test_closest_herbivore()
    test_hunting_and_refueling()
    test_plant_destroyed_without_refueling()
    test_lifespan_death()
    print("ALL PREDATOR TESTS PASSED")
