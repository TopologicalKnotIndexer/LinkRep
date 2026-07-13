"""Ordered join operations in a TopLink representation."""

import json
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkTerm import LinkTerm
except ImportError:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkTerm import LinkTerm


class LinkMethod(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.component_list: list[LinkTerm] = []

    def set_component_list(self, new_component_list: list[LinkTerm]) -> None:
        if not isinstance(new_component_list, list) or any(
            not isinstance(term, LinkTerm) for term in new_component_list
        ):
            raise TypeError("link method must contain LinkTerm objects")
        self.component_list = list(new_component_list)

    @override
    def serialize(self) -> str:
        return "".join(term.serialize() for term in self.component_list)

    @override
    def deserialize(self, s: str) -> None:
        terms = []
        for raw_line in s.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if "#" not in line:
                raise ValueError(f"invalid link method line: {line!r}")
            term = LinkTerm()
            term.deserialize(line)
            terms.append(term)
        self.set_component_list(terms)

    @override
    def json_serialize(self) -> str:
        return json.dumps(
            {
                "type": "LinkMethod",
                "component_list": [
                    json.loads(term.json_serialize()) for term in self.component_list
                ],
            }
        )

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "LinkMethod":
            raise ValueError("JSON object is not a LinkMethod")
        raw = obj.get("component_list")
        if not isinstance(raw, list):
            raise TypeError("LinkMethod.component_list must be a list")
        self.set_component_list(
            [LinkTerm.get_link_term_from_json_str(json.dumps(term)) for term in raw]
        )
