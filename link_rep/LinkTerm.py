"""One component-join term in a TopLink representation."""

import json
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except ImportError:
    from LinkRepMetaObject import LinkRepMetaObject


class LinkTerm(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.component_list: list[list[int]] = []

    def set_component_list(self, new_component_list: list[list[int]]) -> None:
        if not isinstance(new_component_list, list) or len(new_component_list) < 2:
            raise ValueError("a join term requires at least two component references")
        validated: list[list[int]] = []
        for term in new_component_list:
            if not isinstance(term, list) or len(term) != 2:
                raise ValueError("component references must be [factor, component] pairs")
            if any(type(value) is not int or value < 1 for value in term):
                raise ValueError("factor and component indices must be positive integers")
            validated.append(list(term))
        self.component_list = validated

    @override
    def serialize(self) -> str:
        return "#".join(f"L[{left}, {right}]" for left, right in self.component_list) + "\n"

    @override
    def deserialize(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError("link term must be text")
        parsed: list[list[int]] = []
        for raw_term in s.split("#"):
            term = raw_term.strip()
            if not (term.startswith("L[") and term.endswith("]")):
                raise ValueError(f"invalid component reference: {term!r}")
            parts = term[2:-1].split(",")
            if len(parts) != 2:
                raise ValueError("component reference must contain two indices")
            try:
                parsed.append([int(parts[0]), int(parts[1])])
            except ValueError as exc:
                raise ValueError("component indices must be integers") from exc
        self.set_component_list(parsed)

    @override
    def json_serialize(self) -> str:
        return json.dumps({"type": "LinkTerm", "component_list": self.component_list})

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "LinkTerm":
            raise ValueError("JSON object is not a LinkTerm")
        self.set_component_list(obj.get("component_list"))

    @classmethod
    def get_link_term_from_json_str(cls, s: str) -> "LinkTerm":
        item = cls()
        item.json_deserialize(s)
        return item
