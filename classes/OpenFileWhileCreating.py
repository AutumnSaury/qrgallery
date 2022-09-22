# 打开仍在创建中的文件

from time import sleep


class OpenFileWhileCreating:
    def __init__(self, path) -> None:
        self.path = path

    def __enter__(self):
        while not file_completely_created:
            try:
                self.img_file = open(self.path, "rb")
                file_completely_created = True
            # 文件仍在创建，句柄被占用导致尝试打开时发生PermissionError
            except PermissionError:
                sleep(0.25)
        return self.img_file

    def __exit__(self, exc_type, exc_value, traceback):
        self.img_file.close()
