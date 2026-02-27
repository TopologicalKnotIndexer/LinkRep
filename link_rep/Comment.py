from typing_extensions import override
import json

try:
    from .LinkRepMetaObject import LinkRepMetaObject
except:
    from LinkRepMetaObject import LinkRepMetaObject

# 注释部分：记录每一行的注释信息
# 存储的注释信息中不含 "//" 与行末的换行符
class Comment(LinkRepMetaObject):
    def __init__(self) -> None:
        super().__init__()
        self.msg_list = []

    # 设置注释内容
    def set_msg_list(self, new_msg_list:list[str]):
        # 需要删除所有换行符
        self.msg_list = list(map(
            lambda line: line.replace("\n", ""),
            new_msg_list
        ))

    @override
    def serialize(self) -> str:
        return "".join(list(map(
            lambda line: "//" + line + "\n",
            self.msg_list
        )))
    
    @override
    def deserialize(self, s:str) -> None:
        self.set_msg_list([
            item[2:]
            for item in s.split("\n")
            if item.startswith("//")
        ])

    @override
    def json_serialize(self) -> str:
        return json.dumps({
            "type": "Comment",
            "msg_list": self.msg_list
        })
    
    @override
    def json_deserialize(self, s:str) -> None:
        obj_now = json.loads(s)

        # 控制类型
        if obj_now.get("type") != "Comment":
            raise AssertionError()
        
        # 必须包含完整信息
        if not isinstance(obj_now.get("msg_list"), list):
            raise AssertionError()
        
        # 设置元素内容
        self.set_msg_list(obj_now["msg_list"])

if __name__ == "__main__":
    ser = """//line1
//line2 
//line3"""

    obj = Comment()
    obj.deserialize(ser)
    print(obj.json_serialize())
