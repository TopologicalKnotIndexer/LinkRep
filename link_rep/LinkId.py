"""Structured prime-knot or prime-link identifier."""

import json
import re
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except ImportError:  # Direct execution from the package directory.
    from LinkRepMetaObject import LinkRepMetaObject


_LINK_ID = re.compile(r"(?P<mirror>m?)(?P<kind>[LK])(?P<crossings>\d+)(?P<alt>[an])(?P<index>\d+)")


class LinkId(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.mirror = False
        self.knot_or_link = "knot"
        self.alter_or_nonalter = "alter"
        self.crossing_num = 3
        self.inner_index = 1

    def _validate(self) -> None:
        if type(self.mirror) is not bool:
            raise TypeError("mirror must be a boolean")
        if self.knot_or_link not in {"knot", "link"}:
            raise ValueError("knot_or_link must be 'knot' or 'link'")
        if self.alter_or_nonalter not in {"alter", "nonalter"}:
            raise ValueError("alter_or_nonalter has an invalid value")
        if type(self.crossing_num) is not int or self.crossing_num < 0:
            raise ValueError("crossing_num must be a non-negative integer")
        if type(self.inner_index) is not int or self.inner_index < 1:
            raise ValueError("inner_index must be a positive integer")

    @override
    def serialize(self) -> str:
        self._validate()
        return (
            ("m" if self.mirror else "")
            + self.knot_or_link[0].upper()
            + str(self.crossing_num)
            + self.alter_or_nonalter[0].lower()
            + str(self.inner_index)
        )

    @override
    def deserialize(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError("link identifier must be text")
        match = _LINK_ID.fullmatch(s.strip())
        if match is None:
            raise ValueError(f"invalid link identifier: {s!r}")

        # Assign every field, including False, so reusing an instance cannot
        # retain mirror state from a previous document.
        self.mirror = bool(match.group("mirror"))
        self.knot_or_link = "link" if match.group("kind") == "L" else "knot"
        self.alter_or_nonalter = "alter" if match.group("alt") == "a" else "nonalter"
        self.crossing_num = int(match.group("crossings"))
        self.inner_index = int(match.group("index"))
        self._validate()

    @classmethod
    def get_link_id_from_json_str(cls, s: str) -> "LinkId":
        item = cls()
        item.json_deserialize(s)
        return item

    @classmethod
    def get_link_id_from_string(cls, s: str) -> "LinkId":
        item = cls()
        item.deserialize(s)
        return item

    @override
    def json_serialize(self) -> str:
        self._validate()
        return json.dumps(
            {
                "type": "LinkId",
                "mirror": self.mirror,
                "knot_or_link": self.knot_or_link,
                "alter_or_nonalter": self.alter_or_nonalter,
                "crossing_num": self.crossing_num,
                "inner_index": self.inner_index,
            }
        )

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "LinkId":
            raise ValueError("JSON object is not a LinkId")
        required = {
            "mirror",
            "knot_or_link",
            "alter_or_nonalter",
            "crossing_num",
            "inner_index",
        }
        if not required.issubset(obj):
            raise ValueError("LinkId JSON is missing required fields")
        self.mirror = obj["mirror"]
        self.knot_or_link = obj["knot_or_link"]
        self.alter_or_nonalter = obj["alter_or_nonalter"]
        self.crossing_num = obj["crossing_num"]
        self.inner_index = obj["inner_index"]
        self._validate()
