# 不想用SDK，而且换SDK的话要改的东西太多，干脆再写个class算了

import mimetypes
from urllib.parse import urlencode
import requests
from ImgInterface import ImgInterface
from time import time
import re
import hmac
import hashlib


class COSApis(ImgInterface):

    def __init__(self, sk: str, si: str, bucket: str, region: str, last: int) -> None:
        self.key_time = self.__get_key_time(last)
        self.sign_key = self.__hmac_sha1(self.key_time, sk)
        self.si = si
        self.url = bucket + ".cos-website." + region + ".myqcloud.com"

    def upload_img(self, img_file) -> str:
        img_path = img_file.name
        img_name = re.search(r"(?<=\\)[^\\]+\w{3,4}$", img_path).group()
        self.__interpeted_request(
            req_config={
                "url": self.url + "/" + img_name,
                "method": "PUT",
                "headers": {
                    "Content-Type": mimetypes.guess_type(img_file.name)[0],
                    "Content-Length": str(img_file.tell()),
                    "Content-MD5": hashlib.md5(img_file).hexdigest(),
                    "Host": self.url,
                },
                "data": img_file
            },
            keytime=self.key_time,
            sign_key=self.sign_key,
            si=self.si
        )

    def __get_auth(self, si, kt, hl, upl, sign) -> str:
        return "q-sign-algorithm=sha1" \
            + "&q-ak=" + si \
            + "&q-sign-time=" + kt \
            + "&q-key-time=" + kt \
            + "&q-header-list=" + hl \
            + "&q-url-param-list=" + upl \
            + "&q-signature=" + sign

    def __get_key_time(self, last: int) -> str:
        now = int(time())
        return str(now) + ";" + str(now + last)

    def __hmac_sha1(self, key: str, msg: str):
        return hmac.new(bytes(key, encoding="utf-8"), bytes(msg, encoding="utf-8"), hashlib.sha1).hexdigest()

    # 用于生成UrlParamList 和 HttpParameters / HeaderList 和 HttpHeaders
    def __get_kv_str(self, dic) -> tuple:
        kl = {}
        for k, v in dic:
            kl[urlencode(k).lower()] = urlencode(v).lower()
        kl = sorted(kl)
        key_str = ""
        kv_str = ""
        for k, v in kl:
            kv_str += k + "=" + v + "&"
            key_str += k + ";"
        return key_str[0:-1], key_str[0:-1]

    def __get_http_string(self, method, path, hp, hh) -> str:
        return method + "\n" \
            + path + "\n" \
            + hp + "\n" \
            + hh + "\n"

    def __get_sts(self, kt, hs) -> str:
        return "sha1\n" \
            + kt + "\n" \
            + hashlib.sha1(hs).hexdigest() + "\n"

    # 拦截器， 请求发送前插入Authorization头
    def __interpeted_request(self, req_config: dict, key_time: str, sign_key: str, si: str) -> bool:
        if req_config.has_key("params"):
            upl, hp = self.__get_kv_str(req_config["params"])
        else:
            req_config["headers"] = {}
            upl, hp = ("", "")
        if req_config.has_key("params"):
            hl, hh = self.__get_kv_str(req_config["params"])
        else:
            req_config["headers"] = {}
            hl, hh = ("", "")

        hs = self.__get_http_string(req_config["method"].lower(),
                                    re.search(r"(?<=myqcloud\.com)\/.*",
                                              req_config["url"]).group(0),
                                    hp, hh
                                    )
        sts = self.__get_sts(key_time, hs)
        sign = self.__hmac_sha1(sign_key, sts)
        auth = self.__get_auth(si, key_time, hl, upl, sign)

        req_config["headers"]["Authorization"] = auth
        requests.request(**req_config)
