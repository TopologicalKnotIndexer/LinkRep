from typing_extensions import override
import json
import re

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except:
    from LinkRepMetaObject import LinkRepMetaObject

# 存储一个可用的变量名
class LinkId(LinkRepMetaObject):
    def __init__(self) -> None: # default K3a1
        super().__init__()
        self.mirror = False
        self.knot_or_link = "knot"
        self.alter_or_nonalter = "alter"
        self.crossing_num = 3
        self.inner_index = 1

    @override
    def serialize(self) -> str:
        return (
            ("m" if self.mirror else "") + 
            self.knot_or_link[0].upper() +
            str(self.crossing_num) +
            self.alter_or_nonalter[0].lower() +
            str(self.inner_index)
        )
    
    @override
    def deserialize(self, s:str) -> None:
        s = s.strip()

        # 检查名称合法性
        if not re.match(r"^(m|)(L|K)\d+(a|n)\d+$", s):
            raise AssertionError()

        # 检测是不是镜像扭结
        if s[0].lower() == "m": 
            self.mirror = True
            s = s[1:]

        # 检测是不是扭结
        if s[0].lower() == "l":
            self.knot_or_link = "link"
        else:
            self.knot_or_link = "knot"
        s = s[1:]

        # 处理 alter 和非 alter
        if s.find("a") != -1:
            self.alter_or_nonalter = "alter"
            s = s.replace("a", "x")
        else:
            self.alter_or_nonalter = "nonalter"
            s = s.replace("n", "x")

        # 计算编号
        self.crossing_num, self.inner_index = s.split("x")
        self.crossing_num = int(self.crossing_num)
        self.inner_index = int(self.inner_index)

    @classmethod
    def get_link_id_from_json_str(cls, s:str) -> 'LinkId':
        link_id_item = LinkId()
        link_id_item.json_deserialize(s)
        return link_id_item

    @classmethod
    def get_link_id_from_string(cls, s:str) -> 'LinkId':
        link_id_item = LinkId()
        link_id_item.deserialize(s)
        return link_id_item

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "LinkId",
            "mirror": self.mirror,
            "knot_or_link": self.knot_or_link,
            "alter_or_nonalter": self.alter_or_nonalter,
            "crossing_num": self.crossing_num,
            "inner_index": self.inner_index
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "LinkId":
            raise AssertionError()
        
        # 必须包含完整信息
        for item_name in ["mirror", 
                          "knot_or_link", "alter_or_nonalter", "crossing_num", "inner_index"]:
            if not isinstance(obj_now.get(item_name), type(getattr(self, item_name))):
                raise AssertionError()
            setattr(self, item_name, obj_now[item_name])

if __name__ == "__main__":
    link_id = LinkId()
    link_id.json_deserialize('{"type": "LinkId", "mirror": true, "knot_or_link": "link", "alter_or_nonalter": "nonalter", "crossing_num": 5, "inner_index": 3}')
    print(link_id.serialize())
    print(link_id.json_serialize())
