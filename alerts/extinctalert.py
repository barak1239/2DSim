from collections import Counter


class ExtinctAlert:
    def __init__(self, livingent):
        self.trackedtypes = {type(entity) for entity in livingent}
        self.extincttypes = set()

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
        for entitytype in self.trackedtypes:
            if counts[entitytype] == 0 and entitytype not in self.extincttypes:
                print(f"[ALERT] {entitytype.__name__} is extinct!")
                self.extincttypes.add(entitytype)