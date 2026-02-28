from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkId import LinkId
except:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkId import LinkId

# 存储所有的变量定义
class LinkSet(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_list = []

    # 设置变量名的映射关系
    def set_var_list(self, new_var_list:list[LinkId]) -> None:
        self.var_list = new_var_list

    @override
    def serialize(self) -> str:
        return "[" + ", ".join([
            item.serialize()
            for item in self.var_list
        ]) + "]\n"
    
    @override
    def deserialize(self, s:str) -> None:
        s = s.strip()

        if not s.startswith("["):
            raise AssertionError()
        if not s.endswith("]"):
            raise AssertionError()
        
        self.set_var_list([
            LinkId.get_link_id_from_string(item.strip())
            for item in s[1:-1].split(",")
        ])

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkSet",
            "var_list": [
                json.loads(item.json_serialize())
                for item in self.var_list
            ]
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "LinkSet":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("var_list"), list):
            raise AssertionError()

        # 设置元素内容
        self.set_var_list([
            LinkId.get_link_id_from_json_str(json.dumps(item))
            for item in obj_now["var_list"]
        ])

if __name__ == "__main__":
    l1 = LinkId()
    l1.deserialize("L2a1")

    l2 = LinkId()
    l2.deserialize("K3a1")

    l3 = LinkId()
    l3.deserialize("L4a1")

    var_def = LinkSet()
    var_def.set_var_list([l1, l2, l3])

    ser = var_def.serialize()
    print(ser)
    
    new_val = LinkSet()
    new_val.json_deserialize('{"type": "LinkSet", "var_list": [{"type": "LinkId", "mirror": false, "knot_or_link": "link", "alter_or_nonalter": "alter", "crossing_num": 2, "inner_index": 1}, {"type": "LinkId", "mirror": false, "knot_or_link": "link", "alter_or_nonalter": "alter", "crossing_num": 4, "inner_index": 1}, {"type": "LinkId", "mirror": false, "knot_or_link": "knot", "alter_or_nonalter": "alter", "crossing_num": 3, "inner_index": 1}]}')
    print(new_val.json_serialize())
