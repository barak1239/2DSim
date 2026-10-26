from entities.herb import Herb
from entities.predator import Pred


class EatingAlert:
    def update(self, event)->None:
        """

        Args:
            event: dict containig the event type

        Returns: none, just prints the event

        """
        if event["type"] != "entity_eaten":
            return

        eater = event["eater"]
        prey = event["prey"]
        if isinstance(eater, Pred) and isinstance(prey, Herb):
            print(
                f"[ALERT] {type(eater).__name__} ate "
                f"{type(prey).__name__} at ({prey.x}, {prey.y})"
            )