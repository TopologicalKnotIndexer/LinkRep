from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except:
    from LinkRepMetaObject import LinkRepMetaObject

# 存储所有的变量定义
class LinkSet(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.var_list = []

    # 设置变量名的映射关系
    def set_var_list(self, new_var_list:list[str]) -> None:
        self.var_list = new_var_list

    @override
    def serialize(self) -> str:
        return "[" + ", ".join(self.var_list) + "]\n"
    
    @override
    def deserialize(self, s:str) -> None:
        s = s.strip()

        if not s.startswith("["):
            raise AssertionError()
        if not s.endswith("]"):
            raise AssertionError()
        
        self.set_var_list([
            item.strip()
            for item in s[1:-1].split(",")
        ])

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkSet",
            "var_list": self.var_list
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
        self.set_var_list(obj_now["var_list"])

if __name__ == "__main__":
    var_def = LinkSet()
    var_def.set_var_list(["L2a1", "L4a1", "K3a1"])

    ser = var_def.serialize()
    print(ser)
    
    new_val = LinkSet()
    new_val.json_deserialize('{"type": "LinkSet", "var_list": ["L2a1", "L4a1", "K3a1"]}')
    print(new_val.json_serialize())
