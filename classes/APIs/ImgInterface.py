from abc import ABC, abstractmethod
from io import BufferedReader


# 抽象存储API类
# API类需继承该类并实现__init__、auth和upload_img方法
class ImgInterface(ABC):

    @abstractmethod
    # 构造函数
    # 应接受鉴权所需凭据并保存
    def __init__(self):
        pass

    # @abstractmethod
    # # 使用构造时传入的参数鉴权
    # def auth(self) -> None:
    #     pass

    @abstractmethod
    # 上传图片
    # 应接收一个BufferedReader（即图片）作为参数
    # 返回图片url
    def upload_img(self, file: BufferedReader) -> str:
        pass
