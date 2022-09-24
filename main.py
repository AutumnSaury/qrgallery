from urllib.parse import urlencode
from watchdog.observers import Observer
from classes.APIs.COSApis import COSApis
from classes.APIs.LskyApis import LskyApis
from classes.NewPicsHandler import NewPicsHandler
from MyQR import myqr
from classes.Silence import Silence
from classes.OpenFileWhileCreating import OpenFileWhileCreating
from dotenv import load_dotenv
import logging
import platform
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

# 存储后端选择
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND")

if STORAGE_BACKEND == "lsky":

# Lsky API Root
    API_ROOT = os.getenv("API_ROOT")
    USER_INFO = {
        # 用户邮箱
        "email": os.getenv("USREMAIL"),
        # 用户密码
        "password": os.getenv("USERPWD")
    }
    storage = LskyApis(API_ROOT, USER_INFO)
    logging.debug("已设定使用Lsky图床作为存储后端")
elif STORAGE_BACKEND == "cos":
    # 存储桶名称
    BUCKET = os.getenv("BUCKET")
    # 地区
    REGION = os.getenv("REGION")
    # 腾讯云SecretKey
    SECRET_KEY = os.getenv("SECRET_KEY")
    # 腾讯云SecretID
    SECRET_ID = os.getenv("SECRET_ID")
    # 密钥过期时间，单位为秒，默认一天
    LAST_FOR = os.getenv("LAST_FOR", default=86400)

    storage = COSApis(SECRET_KEY, SECRET_ID, BUCKET, REGION, LAST_FOR)
    logging.debug("已设定使用腾讯COS作为存储后端")
else:
    logging.fatal("未设定存储后端")
    exit(1)

# 背景图片路径
BG_PIC = os.getenv("BG_PIC")
# 二维码存放路径
QR_DIR = os.getenv("QR_DIR")
# 照片存放目录
OBSERVED_DIR = os.getenv("OBSERVED_DIR")


def qr_gen(path):
    with OpenFileWhileCreating(path) as img_file:
        img_url = storage.upload_img(img_file)
    img_file_name = re.search(r"(?<=\\)[^\\]+\w{3,4}$", path).group()
    logging.info("已上传图片" + img_file_name +
                 "，图片URL：" + img_url)
    logging.info("正在为图片" + img_file_name + "生成二维码")
    # 关闭myqr成功运行后的line 16: mode: byte输出
    with Silence():
        myqr.run(
            words=img_url,
            version=5,
            picture=BG_PIC,
            colorized=True,
            contrast=1.0,
            brightness=1.0,
            save_name=img_file_name + "_qr.png",
            save_dir=QR_DIR
        )
    logging.info("二维码已保存至" + img_file_name + "_qr.png")
    if platform.system() == "Windows":
        try:
            os.startfile(QR_DIR + "\\" + img_file_name + "_qr.png")
        except:
            raise Exception("尝试打开二维码文件时发生错误")
    else:
        logging.debug("非目标运行环境，未自动打开二维码")

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
