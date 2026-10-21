"""Test herbivore reproduction cooldown without YAML.

Place this file beside the module containing Grid, Herb and Plant.
"""
import random as rnd

# Change the module name if your classes are saved elsewhere.
from sprint2.entity import Grid, Herb, Plant


T_COOLDOWN = 5
SIGHT_RANGE = 0  # During cooldown checks, updates just age and wander randomly.


def count_herbivores(world):
    return sum(isinstance(cell, Herb) for row in world.grid for cell in row)


def main():
    rnd.seed(7)
    world = Grid(7, 7)

    first = Herb(30, 2, 2)
    second = Herb(30, 3, 2)
    plant = Plant(30, 4, 2)
    for entity in (first, second, plant):
        world.addentity(entity)

    # The first parent tries to reach the plant through the second parent.
    first.update(world, 3, T_COOLDOWN,T_HERBIVORE=3)
    assert count_herbivores(world) == 3, "Expected one baby after the first encounter"
    assert (first.cooldown, second.cooldown) == (5, 5), "Both parents need cooldown 5"
    print("Initial reproduction: PASS (3 herbivores, both cooldowns = 5)")

    for turn in range(1, T_COOLDOWN + 1):
        # Deliberately try to enter the other parent's cell BEFORE ticking cooldown.
        # A blocked encounter may cause the first parent to wander to a free cell.
        first.move([(second.x, second.y)], world, T_COOLDOWN,T_HERBIVORE=3)
        assert count_herbivores(world) == 3, f"Unexpected baby during cooldown on turn {turn}"
        assert world.grid[second.x][second.y] is second, "Second parent was overwritten"

        # These updates count down each parent's cooldown, even if it cannot move.
        first.update(world, SIGHT_RANGE, T_COOLDOWN,T_HERBIVORE=3)
        second.update(world, SIGHT_RANGE, T_COOLDOWN,T_HERBIVORE=3)
        assert count_herbivores(world) == 3, f"Unexpected baby on turn {turn}"
        expected = T_COOLDOWN - turn
        assert first.cooldown == expected and second.cooldown == expected, (
            f"Turn {turn}: expected cooldowns {expected}, "
            f"got {first.cooldown} and {second.cooldown}"
        )
        print(f"Cooldown turn {turn}: PASS (cooldowns = {first.cooldown}, {second.cooldown}; 3 herbivores)")

    # Both cooldowns have reached zero: meeting again should create one more baby.
    first.move([(second.x, second.y)], world, T_COOLDOWN,T_HERBIVORE=3)
    assert count_herbivores(world) == 4, "Expected a new baby after cooldown finished"
    assert first.cooldown == T_COOLDOWN and second.cooldown == T_COOLDOWN, (
        "Both parents should restart their cooldown after reproduction"
    )
    print("Reproduction after cooldown: PASS (4 herbivores, cooldowns reset to 5)")
    print("ALL COOLDOWN TESTS PASSED")


if __name__ == "__main__":
    main()
