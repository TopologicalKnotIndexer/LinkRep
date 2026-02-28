from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkId import LinkId
except:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkId import LinkId

# 存储所有的变量定义
class VarDef(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_map = []

    # 设置变量名的映射关系
    # 内层 list 中有两个元素，一个 LinkId 和一个 PdCode
    def set_var_map(self, new_var_map:list[list]) -> None:
        self.var_map = new_var_map
        for item in self.var_map:
            if not isinstance(item, list):
                raise AssertionError()
            if len(item) != 2:
                raise AssertionError()
            if not isinstance(item[0], LinkId):
                raise AssertionError()
            if not isinstance(item[1], list):
                raise AssertionError()

    @override
    def serialize(self) -> str:
        return "".join([
            var_pair[0].serialize() + ": " + json.dumps(var_pair[1]) + "\n"
            for var_pair in self.var_map
        ])
    
    @override
    def deserialize(self, s:str) -> None:
        self.set_var_map([
            [LinkId.get_link_id_from_string(item.split(":")[0].strip())
                ,json.loads(item.split(":")[-1])]
            for item in s.split("\n")
            if item.find(":") != -1
        ])

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "VarDef",
            "var_map": [
                [json.loads(var_pair[0].json_serialize()),
                    var_pair[1]]
                for var_pair in self.var_map
            ]
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "VarDef":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("var_map"), list):
            raise AssertionError()

        # 设置元素内容
        self.set_var_map([
            [LinkId.get_link_id_from_json_str(json.dumps(var_pair[0])),
                var_pair[1]]
            for var_pair in obj_now["var_map"]
        ])

if __name__ == "__main__":
    var_def = VarDef()
    var_def.set_var_map([
        [LinkId.get_link_id_from_string("L2a1"), [[4, 1, 3, 2], [2, 3, 1, 4]]],
        [LinkId.get_link_id_from_string("L4a1"), [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]]
    ])

    ser = var_def.serialize()
    print(ser)
    
    var_def.deserialize(ser)
    print(var_def.json_serialize())
