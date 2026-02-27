from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except:
    from LinkRepMetaObject import LinkRepMetaObject

# 存储所有的变量定义
class VarDef(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_map = dict()

    # 设置变量名的映射关系
    def set_var_map(self, new_var_map:dict[str, list]) -> None:
        self.var_map = new_var_map

    @override
    def serialize(self) -> str:
        return "".join([
            var_name + ": " + json.dumps(self.var_map[var_name]) + "\n"
            for var_name in self.var_map
        ])
    
    @override
    def deserialize(self, s:str) -> None:
        self.set_var_map({
            item.split(":")[0].strip()
                :json.loads(item.split(":")[-1])
            for item in s.split("\n")
            if item.find(":") != -1
        })

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "VarDef",
            "var_map": self.var_map
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "VarDef":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("var_map"), dict):
            raise AssertionError()
        
        # 设置元素内容
        self.set_var_map(obj_now["var_map"])

if __name__ == "__main__":
    var_def = VarDef()
    var_def.set_var_map({
        "L2a1": [[4, 1, 3, 2], [2, 3, 1, 4]],
        "L4a1": [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]
    })

    ser = """L2a1: [[4, 1, 3, 2], [2, 3, 1, 4]]
L4a1: [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]"""
    
    var_def.deserialize(ser)
    print(var_def.json_serialize())
