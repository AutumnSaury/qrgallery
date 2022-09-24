# 不想用SDK，而且换SDK的话要改的东西太多，干脆再写个class算了
from uuid import uuid1
from .ImgInterface import ImgInterface
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class COSApis(ImgInterface):

    def __init__(self, sk: str, si: str, bucket: str, region: str, last: int) -> None:
        self.region = region
        self.bucket = bucket
        self.client = CosS3Client(
            CosConfig(
                Region=region,
                SecretId=si,
                SecretKey=sk
            )
        )

    def upload_img(self, img_file) -> str:
        name = str(uuid1()).upper() + ".jpg"
        self.client.upload_file(
            Bucket=self.bucket,
            Key=name,
            LocalFilePath=img_file.name
        )
        return "https://" + self.bucket + ".cos." + self.region + ".myqcloud.com" + "/" + name
