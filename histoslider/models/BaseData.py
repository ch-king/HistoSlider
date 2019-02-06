import uuid

import jsonpickle


class BaseData:
    def __init__(self, name: str):
        self.id = uuid.uuid4().int
        self.name = name
        self.parent = None
        self.children = dict()

    def _add_child(self, child):
        child.parent = self
        self.children[child.name] = child

    def _delete_child(self, child):
        child.parent = None
        del self.children[child.name]

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json):
        return jsonpickle.decode(json)
