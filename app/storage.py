import datetime
import uuid

from django.core.files.storage import Storage

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class OssStorage(Storage):

    def _save(self, name, content):
        config = CosConfig(Region="ap-nanjing",
                           SecretId="AKIDe6HDsGNEo7AxVnoY2FBpDLCm58uPdbIj",
                           SecretKey="B5j6BzX7SXNwEFzTgcHfmcBTVGjvrVsz", Token=None, Scheme="https")
        client = CosS3Client(config)
        key = f"banners/{datetime.datetime.now().strftime('%Y%m%d')}/{uuid.uuid4()}{name}"
        resp = client.put_object(Bucket="lihood-1306623008",
                                 Body=content,
                                 Key=key)
        return "https://lihood-1306623008.cos.ap-nanjing.myqcloud.com/" + key

    def exists(self, name):
        return False

    def url(self, name):
        return name
