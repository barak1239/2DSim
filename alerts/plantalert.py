from collections import Counter

from entities.plant import Plant


class PlantAlert:
    def __init__(self, grid):
        self.total = grid.width * grid.height
        self.alerted = False

    def update(self, event)->None:
        """
                     Args:
                         event: dict containing the event type

                     Returns: none, just prints the event

                     """
        if event["type"] != "turn_finished":
            return
        livingent = event["entities"]
        counts = Counter(type(entity) for entity in livingent)
        plantcount = counts[Plant]
        if plantcount > self.total * 0.9:
            if not self.alerted:
                print("[ALERT] Plants occupy more than 90% of the grid!")
                self.alerted = True
        else:
            self.alerted = False