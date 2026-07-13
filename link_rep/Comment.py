"""Line comments in a TopLink representation."""

import json
from typing_extensions import override

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except ImportError:
    from LinkRepMetaObject import LinkRepMetaObject


class Comment(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.msg_list: list[str] = []

    def set_msg_list(self, new_msg_list: list[str]):
        if not isinstance(new_msg_list, list) or any(
            not isinstance(line, str) for line in new_msg_list
        ):
            raise TypeError("comment messages must be a list of strings")
        self.msg_list = [line.replace("\r", "").replace("\n", "") for line in new_msg_list]

    @override
    def serialize(self) -> str:
        return "".join("//" + line + "\n" for line in self.msg_list)

    @override
    def deserialize(self, s: str) -> None:
        self.set_msg_list(
            [line[2:] for line in s.splitlines() if line.startswith("//")]
        )

    @override
    def json_serialize(self) -> str:
        return json.dumps({"type": "Comment", "msg_list": self.msg_list})

    @override
    def json_deserialize(self, s: str) -> None:
        obj = json.loads(s)
        if not isinstance(obj, dict) or obj.get("type") != "Comment":
            raise ValueError("JSON object is not a Comment")
        self.set_msg_list(obj.get("msg_list"))
