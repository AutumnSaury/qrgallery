from watchdog.events import FileSystemEventHandler
import re


class NewPicsHandler(FileSystemEventHandler):

    def __init__(self, handler):
        self.handler = handler
        return self

    def handler():
        pass

    def on_created(self, event):
        if re.search(r"(\.jpg)|(\.jpeg)|(\.png)$", event.src_path) != None:
            self.handler()
