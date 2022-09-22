from watchdog.observers import Observer
from classes.APIs.LskyApis import LskyApis
from classes.NewPicsHandler import NewPicsHandler
from MyQR import myqr
from classes.Silence import Silence
from dotenv import load_dotenv
import logging
import os
import re

# 从.env读取环境变量
# 打包前请注释该行
load_dotenv()

# 日志输出设置
logging.basicConfig(
    level=logging.INFO,
    datefmt="%m/%d %H:%M:%S",
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

# Lsky API Root
API_ROOT = os.getenv("API_ROOT")
USER_INFO = {
    # 用户邮箱
    "email": os.getenv("USREMAIL"),
    # 用户密码
    "password": os.getenv("USERPWD")
}
# 背景图片路径
BG_PIC = os.getenv("BG_PIC")
# 二维码存放路径
QR_DIR = os.getenv("QR_DIR")
# 照片存放目录
OBSERVED_DIR = os.getenv("OBSERVED_DIR")

lsky = LskyApis(API_ROOT, USER_INFO)


def qr_gen(path):
    img_info = lsky.upload_img(path)
    img_file_name = re.search(r"(?<=\\)[^\\]+\w{3,4}$", path).group()
    logging.info("已上传图片" + img_file_name +
                 "，图片URL：" + img_info["links"]["url"])
    logging.info("正在为图片" + img_file_name + "生成二维码")
    # 关闭myqr成功运行后的line 16: mode: byte输出
    with Silence():
        myqr.run(
            words=img_info["links"]["url"],
            version=5,
            picture=BG_PIC,
            colorized=True,
            contrast=1.0,
            brightness=1.0,
            save_name=img_info["name"] + "_qr.png",
            save_dir=QR_DIR
        )
    logging.info("二维码已保存至" + img_info["name"] + "_qr.png")
    try:
        os.startfile(QR_DIR + "\\" + img_info["name"] + "_qr.png")
    except:
        raise Exception("尝试打开二维码文件时发生错误")


# 创建并启动Observer线程
ob = Observer()
ob.schedule(NewPicsHandler(qr_gen), OBSERVED_DIR)
logging.info("已启动")
ob.start()

try:
    while ob.is_alive():
        ob.join(1)
finally:
    ob.stop()
    ob.join()
