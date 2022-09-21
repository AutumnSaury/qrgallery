import requests


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

        # self.token = "Bearer " + response.json()["data"]["token"]
        self.api_root = api_root
        self.public_headers = {
            "Authorization": self.token,
            "Accept": "application/json"
        }

    # 上传图片，返回图片URL
    def upload_img(self, path: str):
        try:
            with open(path, "rb") as img_file:
                r = requests.post(
                    self.api_root + "/upload",
                    headers={
                        "Content-Type": "multipart/form-data"
                    } + self.public_headers,
                    files={
                        "file": img_file
                    }
                )
                if not r.json()["status"]:
                    raise Exception()
        except:
            raise Exception("文件上传失败")

        return r.json()["data"]
