import os

from content_tools import settings
from content_tools.libary.verify.sdk import ydm_verify


def test_click_verify():
    file_path = os.path.join(settings.BASE_CLICK_SAME_SHAPE_DIR, "20230830-144122.jpg")
    with open(file_path, 'rb') as f:
        image_content = f.read()
    # 识别
    verify_rs = ydm_verify.YdmVerify().click_verify(image=image_content, verify_type=30101)
    print(verify_rs)