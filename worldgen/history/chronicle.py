"""Chronicle: indexed event log used during sim and exposed via WorldPlan."""

from worldgen.plan import Event


class Chronicle:
    def __init__(self):
        self.events = []
        self._next_id = 0

    def emit(self, year: int, kind: str, text: str, actors: dict = None,
             location_cell: int = -1, attach_to=None):
        eid = self._next_id; self._next_id += 1
        ev = Event(event_id=eid, year=year, kind=kind, text=text,
                   actors=dict(actors or {}), location_cell=location_cell)
        self.events.append(ev)
        # attach_to is a list of (entity, attr) pairs; entity.attr.append(eid)
        if attach_to:
            for entity in attach_to:
                if entity is not None:
                    entity.history_event_ids.append(eid)
        return ev

    def to_list(self):
        return list(self.events)
