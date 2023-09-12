import os
from datetime import datetime

from content_tools import settings
from content_tools.helpers import download


def test_download_image():
    # 测试
    # url = "https://p1-security.byteimg.com/img/security-captcha/slide_c4d407c3c9920fc561656a08971b0e92d929181f_1_1.jpg~tplv-obj.image"
    url = "https://p9-security.byteimg.com/img/security-captcha/slide_bc2c83384ee849389d8ab7c17e23b85db484d7ff_2_1.png~tplv-obj.image"
    filename = "gap"
    result = download.download_image(url, save_directory=settings.BASE_SLIDE_DIR, filename="bg")
    assert result["file_path"] is not None


def test_download_file():
    # 大尺寸视频
    # file = "https://file.suofeiya.com.cn/v/79e00eae-72af-425c-9e15-36465822813d"
    # 小尺寸视频
    file = "https://file.suofeiya.com.cn/v/92edf41e-10dd-4615-b9b7-12f2ab934d7c"
    file_parh = download.download_file(
        file,
        save_directory=settings.BASE_VIDEO_DIR,
        sub_directory=datetime.now().strftime("%Y%m%d"),
        # file_format='mov',
    )
    print(file_parh)
    assert file_parh is not None
