from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .LinkTerm import LinkTerm
except:
    from LinkRepMetaObject import LinkRepMetaObject
    from LinkTerm import LinkTerm

# component list 里面的元素是 LinkTerm
class LinkMethod(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.component_list = []

    # 设置变量名的映射关系
    def set_component_list(self, new_component_list:list[LinkTerm]) -> None:
        self.component_list = new_component_list
        for term in new_component_list:
            if not isinstance(term, LinkTerm):
                raise AssertionError()
            
    @override
    def serialize(self) -> str:
        return "".join(list(map(
            lambda link_term: link_term.serialize(),
            self.component_list
        )))
    
    @override
    def deserialize(self, s:str) -> None:
        new_arr = []
        for term in s.split("\n"):
            if term.find("#") != -1:
                link_term = LinkTerm()
                link_term.deserialize(term.strip())
                new_arr.append(link_term)
        self.set_component_list(new_arr)

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkMethod",
            "component_list": [
                json.loads(link_term.json_serialize())
                for link_term in self.component_list
            ]
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "LinkMethod":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("component_list"), list):
            raise AssertionError()
        
        # 为了纯函数编程
        def map_json_val_to_link_term(json_val:dict) -> LinkTerm:
            link_term = LinkTerm()
            link_term.json_deserialize(json.dumps(json_val))
            return link_term

        # 设置元素内容
        self.set_component_list([
            map_json_val_to_link_term(term)
            for term in obj_now["component_list"]
        ])

if __name__ == "__main__":
    var_def = LinkMethod()
    var_def.deserialize("""\nL[1, 2]#L[2, 3]\nL[1, 3]#L[3, 3]\n""")

    json_str = '{"type": "LinkMethod", "component_list": [{"type": "LinkTerm", "component_list": [[1, 2], [2, 3]]}, {"type": "LinkTerm", "component_list": [[1, 3], [3, 3]]}]}'
    new_link = LinkMethod()
    new_link.json_deserialize(json_str)
    print(new_link.serialize())
