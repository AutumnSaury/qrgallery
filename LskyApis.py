import requests
from time import sleep

class LskyApis:
    # 构造时获取token
    def __init__(self, api_root: str, info: dict) -> None:
        try:
            r = requests.post(
                api_root + "/tokens",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json=info
            )
            if not r.json()["status"]:
                raise Exception()
        except:
            raise Exception("尝试登录时发生网络错误")

        self.token = "Bearer " + r.json()["data"]["token"]
        self.api_root = api_root
        self.public_headers = {
            "Authorization": self.token,
            "Accept": "application/json"
        }

    # 上传图片，返回图片URL
    def upload_img(self, path: str):
        # 尝试打开文件，若仍在创建则0.25秒后重试
        file_completely_created = False
        while not file_completely_created:
            try:
                img_file = open(path, "rb")
                file_completely_created = True
            # 文件仍在创建，句柄被占用导致尝试打开时发生PermissionError
            except PermissionError:
                sleep(0.25)
            except:
                raise Exception("权限错误，无法上传图片")
        # 上传打开的图片
        try:
            r = requests.post(
                self.api_root + "/upload",
                headers=self.public_headers,
                files={
                    "file": img_file
                }
            )
            if not r.json()["status"]:
                raise Exception()
        except:
            raise Exception("文件上传失败")
        # 关闭文件句柄
        finally:
            img_file.close()

        return r.json()["data"]
