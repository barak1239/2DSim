"""small standalone test for ApexPredator movement and eating.

"""

from entities.predator import Pred
from grid import Grid

try:
    from entities.apexpredator import ApexPredator
except ModuleNotFoundError:
    from entities.apexpredator import ApexPredator


def test_apex_predator_eats_predator():
    world = Grid(5, 5)
    apex = ApexPredator(8, 2, 2)
    pred = Pred(6, 2, 3)

    world.addentity(apex)
    world.addentity(pred)

    path = apex.look(4, world)
    print("Path to predator:", path)
    assert path == [(2, 3)], f"Expected [(2, 3)], got {path}"

    apex.move(path, world, 5, 8)

    assert (apex.x, apex.y) == (2, 3), "Apex predator did not move to the predator's cell"
    assert world.grid[2][3] is apex, "Grid doesn't contain the apex predator at (2, 3)"
    assert world.grid[2][2] is None, "Apex predator's old cell is not empty"
    assert apex.steps == 14, f"Expected 14 lifetime steps (8 + 6), got {apex.steps}"

    print("PASS: Apex predator found, moved to, and ate the predator.")


if __name__ == "__main__":
    test_apex_predator_eats_predator()
