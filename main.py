from watchdog.observers import Observer
from LskyApis import LskyApis
from NewPicsHandler import NewPicsHandler
from MyQR import myqr
import os

# 以下配置项请在打包前进行修改
# Lsky API Root
API_ROOT = ""
USER_INFO = {
    # 用户邮箱
    "email": "",
    # 用户密码
    "password": ""
}
# 背景图片路径
BG_PIC = r""
# 二维码存放路径
QR_DIR = r""
# 照片存放目录
OBSERVED_DIR = r""

lsky = LskyApis(API_ROOT, USER_INFO)


def qr_gen(path):
    img_info = lsky.upload_img(path)
    myqr.run(
        words=img_info["links"]["url"],
        version=5,
        picture=BG_PIC,
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=img_info["name"] + "qr.png",
        save_dir=QR_DIR
    )
    try:
        os.startfile(QR_DIR + "\\" + img_info["name"] + "qr.png")
    except:
        raise Exception("尝试打开二维码文件时发生错误")


ob = Observer()
ob.schedule(NewPicsHandler(qr_gen), OBSERVED_DIR)
ob.start()

try:
    while ob.is_alive():
        ob.join(1)
finally:
    ob.stop()
    ob.join()
