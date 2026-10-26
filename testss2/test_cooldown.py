"""check cooldown and reproduction using the Sprint 3 method signatures."""
from unittest.mock import patch

from entities.herb import Herb
from grid import Grid

T_COOLDOWN = 5
BABY_LIFESPAN = 12
PARAMETERS = {"R_HERBIVORE_SIGHT": 0, "R_PREDATOR_SIGHT": 3,
              "T_HERBIVORE": BABY_LIFESPAN, "T_PREDATOR": 6,
              "T_COOLDOWN": T_COOLDOWN}


def count_herbivores(world):
    return sum(isinstance(cell, Herb) for row in world.grid for cell in row)


def test_cooldown():
    world = Grid(7, 7)
    first, second = Herb(30, 2, 2), Herb(30, 3, 2)
    world.addentity(first)
    world.addentity(second)

    # Trigger a deliberate encounter; no reliance on random BFS choices.
    first.move([(3, 2)], world, T_COOLDOWN, BABY_LIFESPAN)
    assert count_herbivores(world) == 3
    assert (first.cooldown, second.cooldown) == (5, 5)

    for turn in range(1, T_COOLDOWN + 1):
        # Still on cooldown before the turn begins.
        first.move([(second.x, second.y)], world, T_COOLDOWN, BABY_LIFESPAN)
        assert count_herbivores(world) == 3
        # Keep both stationary; test cooldown, not random wandering.
        with patch.object(first, "look", return_value=None), patch.object(second, "look", return_value=None):
            first.update(world, PARAMETERS)
            second.update(world, PARAMETERS)
        expected = T_COOLDOWN - turn
        assert (first.cooldown, second.cooldown) == (expected, expected)
        print(f"Cooldown turn {turn}: PASS")

    first.move([(second.x, second.y)], world, T_COOLDOWN, BABY_LIFESPAN)
    assert count_herbivores(world) == 4
    assert (first.cooldown, second.cooldown) == (5, 5)
    print("PASS: Reproduction works again when cooldown reaches zero")


if __name__ == "__main__":
    test_cooldown()
