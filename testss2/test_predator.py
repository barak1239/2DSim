"""Small, repeatable tests for the current predator logic (no YAML needed).
"""

import random as rnd

PARAMETERS = {"R_HERBIVORE_SIGHT": 4, "R_PREDATOR_SIGHT": 4, "T_HERBIVORE": 12, "T_PREDATOR": 6, "T_COOLDOWN": 5}

from entities.herb import Herb
from entities.plant import Plant
from entities.predator import Pred
from grid import Grid


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

    predator.update(world, PARAMETERS)
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
    predator.move([(2, 3)], world, 5, 12)

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

    predator.update(world, PARAMETERS)

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
def test_predator_eventual_extinction():
    """Verify that predators eventually die without food."""
    world = Grid(7, 7)

    predators = [
        Pred(6, 1, 1),
        Pred(6, 3, 3),
        Pred(6, 5, 5),
    ]

    for predator in predators:
        world.addentity(predator)

    rnd.seed(42)

    assert count_type(world, Pred) == 3

    # No herbivores exist, so predators cannot refuel.
    # After 6 turns, all predators should be dead.
    for turn in range(6):
        for predator in predators:
            if world.grid[predator.x][predator.y] is predator:
                predator.update(world, PARAMETERS)

        print(
            f"Turn {turn + 1}: "
            f"{count_type(world, Pred)} predators remaining"
        )

    assert count_type(world, Pred) == 0, (
        "Predators should become extinct after 6 turns without food"
    )

    print("Predator extinction: PASS (all predators died without food)")


if __name__ == "__main__":
    test_closest_herbivore()
    test_hunting_and_refueling()
    test_plant_destroyed_without_refueling()
    test_lifespan_death()
    test_predator_eventual_extinction()
    print("ALL PREDATOR TESTS PASSED")
