"""Tests for PlantAlert's >90% threshold and Observer behavior."""

from alerts.eventmanager import EventManager
from alerts.plantalert import PlantAlert
from entities.plant import Plant
from grid import Grid


def make_world(plant_count, width=10, height=10):
    """Create a grid with exactly plant_count living plants."""
    world = Grid(width, height)
    for index in range(plant_count):
        x, y = divmod(index, width)
        world.addentity(Plant(10, x, y))
    return world


def turn_event(world):
    """Build the same turn_finished event as the simulation."""
    return {
        "type": "turn_finished",
        "entities": [cell for row in world.grid for cell in row if cell is not None],
    }


def test_below_90_percent_no_alert(capsys):
    world = make_world(89)
    alert = PlantAlert(world)

    alert.update(turn_event(world))

    assert "[ALERT]" not in capsys.readouterr().out


def test_exactly_90_percent_no_alert(capsys):
    world = make_world(90)
    alert = PlantAlert(world)

    alert.update(turn_event(world))

    assert "[ALERT]" not in capsys.readouterr().out


def test_above_90_percent_alert(capsys):
    world = make_world(91)
    alert = PlantAlert(world)

    alert.update(turn_event(world))

    output = capsys.readouterr().out
    assert output.count("[ALERT]") == 1
    assert "90%" in output


def test_alert_not_repeated_on_consecutive_turns(capsys):
    world = make_world(95)
    alert = PlantAlert(world)

    alert.update(turn_event(world))
    alert.update(turn_event(world))
    alert.update(turn_event(world))

    assert capsys.readouterr().out.count("[ALERT]") == 1


def test_alert_rearms_after_plant_count_drops(capsys):
    world = make_world(91)
    alert = PlantAlert(world)

    alert.update(turn_event(world))  # Above threshold: first alert
    world.remove(world.grid[0][0])  # Exactly 90%: reset
    alert.update(turn_event(world))
    world.addentity(Plant(10, 0, 0))  # Above threshold again
    alert.update(turn_event(world))

    assert capsys.readouterr().out.count("[ALERT]") == 2


def test_ignores_unrelated_events(capsys):
    world = make_world(91)
    alert = PlantAlert(world)

    alert.update({"type": "entity_eaten", "eater": None, "prey": None})

    assert capsys.readouterr().out == ""


def test_event_manager_notifies_plant_alert(capsys):
    world = make_world(91)
    manager = EventManager()
    manager.addObserver(PlantAlert(world))

    manager.notifyObservers(turn_event(world))

    assert capsys.readouterr().out.count("[ALERT]") == 1
