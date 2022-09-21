from watchdog.events import FileSystemEventHandler
import re


class NewPicsHandler(FileSystemEventHandler):

    def __init__(self, handler):
        self.handler = handler

    # 处理图片上传和二维码生成，接收图片路径作为参数
    def handler(path):
        pass

    def on_created(self, event):
        if re.search(r"(\.jpg)|(\.jpeg)|(\.png)$", event.src_path):
            self.handler(event.src_path)
