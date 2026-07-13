"""Named PD-code definitions in a TopLink representation."""

from collections import Counter
import json
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkId import LinkId
except ImportError:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkId import LinkId


def _valid_pd_code(pd_code: object) -> bool:
    if not isinstance(pd_code, list):
        return False
    labels = []
    label_type = None
    for crossing in pd_code:
        if not isinstance(crossing, list) or len(crossing) != 4:
            return False
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, (int, str)):
                return False
            if label_type is None:
                label_type = type(label)
            elif type(label) is not label_type:
                return False
            labels.append(label)
    return all(count == 2 for count in Counter(labels).values())


class VarDef(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_map: list[list] = []

    def set_var_map(self, new_var_map: list[list]) -> None:
        if not isinstance(new_var_map, list):
            raise TypeError("variable definitions must be a list")
        validated = []
        names = set()
        for item in new_var_map:
            if not isinstance(item, list) or len(item) != 2:
                raise ValueError("each variable definition must contain name and PD code")
            link_id, pd_code = item
            if not isinstance(link_id, LinkId):
                raise TypeError("variable name must be a LinkId")
            if not _valid_pd_code(pd_code):
                raise ValueError(f"invalid PD code for {link_id.serialize()}")
            name = link_id.serialize()
            if name in names:
                raise ValueError(f"duplicate variable definition: {name}")
            names.add(name)
            validated.append([link_id, pd_code])
        self.var_map = validated

    @override
    def serialize(self) -> str:
        return "".join(
            link_id.serialize() + ": " + json.dumps(pd_code) + "\n"
            for link_id, pd_code in self.var_map
        )

    @override
    def deserialize(self, s: str) -> None:
        parsed = []
        for raw_line in s.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if ":" not in line:
                raise ValueError(f"invalid variable definition: {line!r}")
            name, raw_pd_code = line.split(":", 1)
            parsed.append(
                [LinkId.get_link_id_from_string(name.strip()), json.loads(raw_pd_code)]
            )
        self.set_var_map(parsed)

    @override
    def json_serialize(self) -> str:
        return json.dumps(
            {
                "type": "VarDef",
                "var_map": [
                    [json.loads(link_id.json_serialize()), pd_code]
                    for link_id, pd_code in self.var_map
                ],
            }
        )

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "VarDef":
            raise ValueError("JSON object is not a VarDef")
        raw = obj.get("var_map")
        if not isinstance(raw, list):
            raise TypeError("VarDef.var_map must be a list")
        parsed = []
        for pair in raw:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError("invalid VarDef entry")
            parsed.append(
                [LinkId.get_link_id_from_json_str(json.dumps(pair[0])), pair[1]]
            )
        self.set_var_map(parsed)
