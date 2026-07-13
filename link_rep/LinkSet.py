"""Ordered factor list in a TopLink representation."""

import json
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkId import LinkId
except ImportError:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkId import LinkId


class LinkSet(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_list: list[LinkId] = []

    def set_var_list(self, new_var_list: list[LinkId]) -> None:
        if not isinstance(new_var_list, list) or any(
            not isinstance(item, LinkId) for item in new_var_list
        ):
            raise TypeError("factor list must contain LinkId objects")
        self.var_list = list(new_var_list)

    @override
    def serialize(self) -> str:
        return "[" + ", ".join(item.serialize() for item in self.var_list) + "]\n"

    @override
    def deserialize(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError("factor set must be text")
        text = s.strip()
        if not (text.startswith("[") and text.endswith("]")):
            raise ValueError("factor set must be enclosed in brackets")
        body = text[1:-1].strip()
        self.set_var_list(
            []
            if not body
            else [LinkId.get_link_id_from_string(item.strip()) for item in body.split(",")]
        )

    @override
    def json_serialize(self) -> str:
        return json.dumps(
            {
                "type": "LinkSet",
                "var_list": [json.loads(item.json_serialize()) for item in self.var_list],
            }
        )

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "LinkSet":
            raise ValueError("JSON object is not a LinkSet")
        raw = obj.get("var_list")
        if not isinstance(raw, list):
            raise TypeError("LinkSet.var_list must be a list")
        self.set_var_list(
            [LinkId.get_link_id_from_json_str(json.dumps(item)) for item in raw]
        )
