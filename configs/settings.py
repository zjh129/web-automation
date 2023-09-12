import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# stealth.min.js的路径
STEALTH_JS_PATH = os.path.join(BASE_DIR, "resource", "js", "stealth.min.js")
# 扫码登录二维码图片文件路径
BASE_SCAN_LOGIN_QRCODE_DIR = os.path.join(BASE_DIR, "storage", "scan_login_qrcode")
# 上传文件的路径
BASE_STORAGE_DIR = os.path.join(BASE_DIR, "storage", "upload")
# 视频下载文件路径
BASE_VIDEO_DIR = os.path.join(BASE_DIR, "storage", "video")
# 图片下载文件路径
BASE_IMAGE_DIR = os.path.join(BASE_DIR, "storage", "image")
# 封面图片文件路径
BASE_COVER_DIR = os.path.join(BASE_DIR, "storage", "cover")
# 滑块图片文件路径
BASE_SLIDE_DIR = os.path.join(BASE_DIR, "storage", "slide")
#  按顺序点击文字图片文件存储路径
BASE_CLICK_WORD_DIR = os.path.join(BASE_DIR, "storage", "click_word")
# 点击两个相同形状的物体文件存储路径
BASE_CLICK_SAME_SHAPE_DIR = os.path.join(BASE_DIR, "storage", "click_same_shape")