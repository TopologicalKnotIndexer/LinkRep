from abc import ABC, abstractmethod

class LinkRepMetaObject(ABC):
    def __init__(self) -> None:
        pass
    
    # 标准字符串序列号化
    @abstractmethod
    def serialize(self) -> str:
        return ""
    
    # 标准字符串反序列化
    @abstractmethod
    def deserialize(self, s:str) -> None:
        return
    
    # JSON 字符串序列号化
    @abstractmethod
    def json_serialize(self) -> str:
        return ""
    
    # JSON 字符串反序列化
    @abstractmethod
    def json_deserialize(self, s:str) -> None:
        return
