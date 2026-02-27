from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
    from .Comment import Comment
    from .VarDef import VarDef
    from .LinkSet import LinkSet
    from .LinkMethod import LinkMethod
except:
    from LinkRepMetaObject import LinkRepMetaObject
    from Comment import Comment
    from VarDef import VarDef
    from LinkSet import LinkSet
    from LinkMethod import LinkMethod

# 存储所有的变量定义
class LinkRep(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.comment = Comment()
        self.var_def = VarDef()
        self.link_set = LinkSet()
        self.link_method = LinkMethod()

    @override
    def serialize(self) -> str:
        return (
            self.comment.serialize() +
            self.var_def.serialize() +
            self.link_set.serialize() +
            self.link_method.serialize()
        )
    
    @override
    def deserialize(self, s:str) -> None:
        s = s.strip()

        comment_list = []
        var_def_list = []
        link_method_list = []
        link_set_list = []
        for line in s.split("\n"):
            line = line.strip()
            if line == "":
                continue
            if line.startswith("//"):
                comment_list.append(line)
            elif line.find(":") != -1:
                var_def_list.append(line)
            elif line.find("#") != -1:
                link_method_list.append(line)
            elif line.startswith("[") and line.endswith("]"):
                link_set_list.append(line)
            else:
                raise AssertionError()
        
        if len(link_set_list) != 1:
            raise AssertionError()

        # 依次对所有元素进行反序列化
        self.comment.deserialize("\n".join(comment_list))
        self.var_def.deserialize("\n".join(var_def_list))
        self.link_set.deserialize(link_set_list[0])
        self.link_method.deserialize("\n".join(link_method_list))

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkRep",
            "comment": json.loads(self.comment.json_serialize()),
            "var_def": json.loads(self.var_def.json_serialize()),
            "link_set": json.loads(self.link_set.json_serialize()),
            "link_method": json.loads(self.link_method.json_serialize())
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "LinkRep":
            raise AssertionError()
        
        # 必须包含完整信息
        for term_name in ["comment", "var_def", "link_set", "link_method"]:
            if not isinstance(obj_now.get(term_name), dict):
                raise AssertionError()

            instance_now = self.__getattribute__(term_name)
            if not isinstance(instance_now, LinkRepMetaObject):
                raise AssertionError()
            instance_now.json_deserialize(json.dumps(obj_now.get(term_name)))

if __name__ == "__main__":
    real_serial = (
"""
// this is comment line 1
// this is comment line 2
L2a1: [[4, 1, 3, 2], [2, 3, 1, 4]]
L4a1: [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]
K3a1: [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
[L2a1, L4a1, K3a1]
L[1, 1]#L[2, 1]
L[2, 2]#L[3, 1]
""").lstrip()
    
    rev_obj = LinkRep()
    rev_obj.deserialize(real_serial)
    assert rev_obj.serialize() == real_serial

    json_serialize = rev_obj.json_serialize()
    rev_obj_2 = LinkRep()
    rev_obj_2.json_deserialize(json_serialize)

    assert rev_obj_2.serialize() == real_serial
    assert rev_obj_2.json_serialize() == rev_obj.json_serialize()

    print(rev_obj_2.serialize())
