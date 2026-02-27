from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except:
    from LinkRepMetaObject import LinkRepMetaObject

# 这个 component_list 里面放的东西是一个 list of list
# 每个 sub_list 中有两个整数，L[i, j] 中的 i, j
class LinkTerm(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.component_list = []

    # 设置变量名的映射关系
    def set_component_list(self, new_component_list:list[list[int]]) -> None:
        self.component_list = new_component_list
        for term in new_component_list:
            if not isinstance(term, list):
                raise AssertionError()
            if len(term) != 2:
                raise AssertionError()
            for sub_term in term:
                if not isinstance(sub_term, int):
                    raise AssertionError()
            
    @override
    def serialize(self) -> str:
        return "#".join(list(map(
            lambda pr: f"L[{pr[0]}, {pr[1]}]", # 把连通分量编号
            self.component_list
        ))) + "\n"
    
    @override
    def deserialize(self, s:str) -> None:
        new_arr = []
        for term in s.split("#"):
            term = term.strip()
            if term == "":
                raise AssertionError()
            if not (term.startswith("L[") and term.endswith("]")):
                raise AssertionError()
            li, ri = term[2:-1].split(",")
            new_arr.append([int(li), int(ri)])
        self.set_component_list(new_arr)

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkTerm",
            "component_list": self.component_list
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "LinkTerm":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("component_list"), list):
            raise AssertionError()
        
        # 设置元素内容
        self.set_component_list(obj_now["component_list"])

if __name__ == "__main__":
    var_def = LinkTerm()
    var_def.set_component_list([[1, 1], [2, 1], [3, 2]])

    ser = var_def.serialize()
    print(ser)

    new_var = LinkTerm()
    new_var.deserialize("L[1, 1]#L[2, 1]#L[3, 2]")
    print(new_var.json_serialize())
