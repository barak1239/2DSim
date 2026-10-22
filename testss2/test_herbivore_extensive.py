"""Extensive herbivore tests for the GameOfLife project.

Put this file alongside grid.py, mobileentity.py, plant.py, entity.py and block.py.
Run: python -m unittest -v test_herbivore_extensive.py

These tests are independent of YAML and the 590-entity simulation.
Tests marked EXPECTED BEHAVIOR express ecosystem requirements. If one fails,
it identifies a behavior to inspect, not necessarily a syntax error.
"""

import unittest

from entities.mobileentity import Herb, Pred
from grid import Grid
from entities.plant import Plant
from entities.block import Rock, Tree

SIGHT = 4
COOLDOWN = 5
BABY_LIFESPAN = 12


def occupants(world, cls):
    return [e for row in world.grid for e in row if isinstance(e, cls)]


def place(world, *entities):
    for entity in entities:
        assert 0 <= entity.x < world.height and 0 <= entity.y < world.width
        assert world.grid[entity.x][entity.y] is None, (entity.x, entity.y)
        world.addentity(entity)
    return world


def is_present(world, entity):
    return world.grid[entity.x][entity.y] is entity


class TestHerbivoreBasics(unittest.TestCase):
    def test_01_herbivore_initial_values(self):
        herb = Herb(12, 1, 2)
        self.assertEqual((herb.x, herb.y, herb.steps, herb.cooldown), (1, 2, 12, 0))

    def test_02_no_food_one_move_per_update(self):
        world = place(Grid(7, 7), Herb(12, 3, 3))
        herb = world.grid[3][3]
        herb.update(world, 2, COOLDOWN, BABY_LIFESPAN)
        self.assertLessEqual(max(abs(herb.x - 3), abs(herb.y - 3)), 1)
        self.assertEqual(herb.steps, 11)
        self.assertTrue(is_present(world, herb))
        self.assertEqual(len(occupants(world, Herb)), 1)

    def test_03_herb_dies_after_lifespan_expires(self):
        world = place(Grid(3, 3), Herb(1, 1, 1))
        herb = world.grid[1][1]
        herb.update(world, 1, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual(herb.steps, 0)
        self.assertEqual(len(occupants(world, Herb)), 0)

    def test_04_herb_can_remain_stationary_if_trapped(self):
        world = Grid(3, 3)
        herb = Herb(10, 1, 1)
        place(world, herb)
        for x in range(3):
            for y in range(3):
                if (x, y) != (1, 1):
                    world.addentity(Rock(x, y))
        herb.update(world, 2, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual((herb.x, herb.y), (1, 1))
        self.assertEqual(herb.steps, 9)

    def test_05_herb_cannot_overwrite_rock_or_tree(self):
        world = place(Grid(3, 3), Herb(10, 1, 1), Rock(0, 0), Tree(0, 1))
        herb = world.grid[1][1]
        for _ in range(5):
            herb.update(world, 1, COOLDOWN, BABY_LIFESPAN)
            self.assertIsInstance(world.grid[0][0], Rock)
            self.assertIsInstance(world.grid[0][1], Tree)


class TestHerbivoreFoodAndBFS(unittest.TestCase):
    def test_06_adjacent_plant_is_eaten_and_refuels(self):
        world = place(Grid(5, 5), Herb(5, 2, 2), Plant(7, 2, 3))
        herb = world.grid[2][2]
        herb.update(world, SIGHT, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual((herb.x, herb.y), (2, 3))
        self.assertEqual(herb.steps, 5 + 7 - 1)
        self.assertEqual(len(occupants(world, Plant)), 0)

    def test_07_nearest_plant_selected(self):
        world = place(Grid(7, 7), Herb(8, 3, 3), Plant(8, 3, 5), Plant(8, 6, 6))
        herb = world.grid[3][3]
        path = herb.look(5, world)
        self.assertEqual(path[-1], (3, 5))
        self.assertEqual(len(path), 2)

    def test_08_sight_limit_prevents_targeting_distant_plant(self):
        world = place(Grid(9, 9), Herb(8, 0, 0), Plant(8, 8, 8))
        herb = world.grid[0][0]
        path = herb.look(1, world)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 1)  # random fallback, not long-distance path
        self.assertNotEqual(path[-1], (8, 8))

    def test_09_rock_wall_blocks_path_to_food(self):
        world = place(Grid(3, 3), Herb(8, 0, 0), Plant(8, 2, 2))
        herb = world.grid[0][0]
        # 8-way movement means complete blocking requires all exit neighbors.
        for x, y in [(0, 1), (1, 0), (1, 1)]:
            world.addentity(Rock(x, y))
        self.assertIsNone(herb.look(5, world))
        herb.update(world, 5, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual((herb.x, herb.y), (0, 0))

    def test_10_diagonal_plant_is_one_step_away(self):
        world = place(Grid(5, 5), Herb(8, 2, 2), Plant(8, 3, 3))
        herb = world.grid[2][2]
        self.assertEqual(herb.look(1, world), [(3, 3)])

    def test_11_herb_does_not_refuel_on_empty_cell(self):
        world = place(Grid(5, 5), Herb(7, 2, 2))
        herb = world.grid[2][2]
        herb.update(world, 2, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual(herb.steps, 6)


class TestHerbivoreReproduction(unittest.TestCase):
    def test_12_direct_reproduce_adds_one_baby_full_lifespan(self):
        world = place(Grid(5, 5), Herb(3, 2, 2))
        parent = world.grid[2][2]
        self.assertTrue(parent.reproduce(world, BABY_LIFESPAN))
        babies = [h for h in occupants(world, Herb) if h is not parent]
        self.assertEqual(len(babies), 1)
        baby = babies[0]
        self.assertEqual(baby.steps, BABY_LIFESPAN)
        self.assertEqual(baby.cooldown, 0)
        self.assertLessEqual(max(abs(baby.x - parent.x), abs(baby.y - parent.y)), 1)
        self.assertTrue(is_present(world, parent))

    def test_13_cooldown_blocks_direct_reproduction(self):
        world = place(Grid(5, 5), Herb(12, 2, 2))
        parent = world.grid[2][2]
        parent.cooldown = 3
        self.assertFalse(parent.reproduce(world, BABY_LIFESPAN))
        self.assertEqual(len(occupants(world, Herb)), 1)

    def test_14_full_neighborhood_prevents_baby(self):
        world = Grid(3, 3)
        parent = Herb(12, 1, 1)
        place(world, parent)
        for x in range(3):
            for y in range(3):
                if (x, y) != (1, 1):
                    world.addentity(Rock(x, y))
        self.assertFalse(parent.reproduce(world, BABY_LIFESPAN))
        self.assertEqual(len(occupants(world, Herb)), 1)

    def test_15_encounter_reproduces_if_path_starts_with_other_herb(self):
        # A plant behind the other herb makes the BFS return a path through it.
        world = place(Grid(5, 5), Herb(8, 2, 1), Herb(9, 2, 2), Plant(7, 2, 3))
        parent_a = world.grid[2][1]
        parent_b = world.grid[2][2]
        # Block shorter alternate ways to reach the plant.
        for x, y in [(1, 2), (1, 3), (3, 2), (3, 3)]:
            world.addentity(Rock(x, y))
        self.assertEqual(parent_a.look(4, world)[0], (2, 2))
        parent_a.update(world, 4, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual(len(occupants(world, Herb)), 3)
        self.assertTrue(is_present(world, parent_a))
        self.assertTrue(is_present(world, parent_b))
        self.assertEqual(parent_a.cooldown, COOLDOWN)
        self.assertEqual(parent_b.cooldown, COOLDOWN)
        baby = next(h for h in occupants(world, Herb) if h not in (parent_a, parent_b))
        self.assertEqual(baby.steps, BABY_LIFESPAN)
        self.assertEqual(parent_a.steps, 7)  # reproduction consumes one turn

    def test_16_diagnostic_reproduction_without_nearby_plants(self):
        """OPTIONAL DESIGN EXPECTATION, not an unambiguous assignment rule.

        If you expect neighboring herbivores to seek mates even when no
        plants are visible, this detects whether look() can target one.
        Your current BFS only targets self.foodtype (Plant), so it will
        generally choose an empty random cell instead of the other herb.
        """
        world = place(Grid(5, 5), Herb(8, 2, 2), Herb(8, 2, 3))
        a = world.grid[2][2]
        path = a.look(1, world)

    def test_17_baby_does_not_act_in_birth_turn_snapshot(self):
        world = place(Grid(5, 5), Herb(8, 2, 1), Herb(8, 2, 2), Plant(7, 2, 3))
        a, b = world.grid[2][1], world.grid[2][2]
        for x, y in [(1, 2), (1, 3), (3, 2), (3, 3)]:
            world.addentity(Rock(x, y))
        snapshot = occupants(world, Herb)
        a.update(world, 4, COOLDOWN, BABY_LIFESPAN)
        babies = [h for h in occupants(world, Herb) if h not in (a, b)]
        self.assertEqual(len(babies), 1)
        self.assertNotIn(babies[0], snapshot)
        self.assertEqual(babies[0].steps, BABY_LIFESPAN)

    def test_18_encounter_on_cooldown_does_not_spawn(self):
        world = place(Grid(5, 5), Herb(8, 2, 1), Herb(8, 2, 2), Plant(7, 2, 3))
        a, b = world.grid[2][1], world.grid[2][2]
        a.cooldown = 3
        for x, y in [(1, 2), (1, 3), (3, 2), (3, 3)]:
            world.addentity(Rock(x, y))
        a.update(world, 4, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual(len(occupants(world, Herb)), 2)
        self.assertEqual(a.cooldown, 2)
        self.assertEqual(b.cooldown, 0)


class TestHerbivorePredatorInteractions(unittest.TestCase):
    def test_19_predator_eats_herbivore(self):
        world = place(Grid(5, 5), Pred(5, 2, 2), Herb(7, 2, 3))
        pred = world.grid[2][2]
        victim = world.grid[2][3]
        pred.update(world, SIGHT, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual((pred.x, pred.y), (2, 3))
        self.assertEqual(pred.steps, 5 + 7 - 1)
        self.assertFalse(is_present(world, victim))
        self.assertEqual(len(occupants(world, Herb)), 0)

    def test_20_no_herbivore_creation_from_predator(self):
        world = place(Grid(5, 5), Pred(7, 2, 2))
        pred = world.grid[2][2]
        pred.update(world, SIGHT, COOLDOWN, BABY_LIFESPAN)
        self.assertEqual(len(occupants(world, Herb)), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
