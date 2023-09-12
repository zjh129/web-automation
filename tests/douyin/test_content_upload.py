from datetime import datetime, timedelta

from content_tools.helpers import log
from content_tools.libary.douyin.creator_content import CreatorContent


def test_upload_video():
    """
    测试视频上传
    """
    request = {
        'user_id': '19106013803',
        'video': "https://file.suofeiya.com.cn/v/92edf41e-10dd-4615-b9b7-12f2ab934d7c",
        "desc": "开心的办公室摆拍",
        # "cover": "https://file.suofeiya.com.cn/v/9eb7472c-a968-4f52-9bc2-602b7870cedf",
        "cover": "https://file.suofeiya.com.cn/v/62e69684-3955-4a3d-9038-cbe0fbbb3465",
        "sync_to_toutiao": True,
        "allow_download": False,
        "who_can_watch": "fans",
        "publish_time": {
            "type": "delay",
            "time": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M"),
        },
    }
    create_content = CreatorContent(user_id=request.get("user_id"), save_state=True, brower_headless=False, browser_devtools=True, slow_mo=200)
    # 调用发送验证码方法
    response = create_content.upload_video(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")

def test_upload_image_text():
    """
    测试图文上传
    """
    request = {
        'user_id': '19106013803',
        'title': "绿色的回忆",
        'desc': "我小时候的老家白杨树林真是美极了！那里简直是欢乐和快乐的代名词。高大的白杨树在阳光下闪闪发亮，笑声在树林里回荡不止。这些白杨树见证了我的成长，成为了我永远不会忘记的回忆。老家的风景就像一个童话乐园，对我来说真是太宝贵了！#家乡风景 #白杨树林 #童年回忆",
        'image_list': [
            "https://file.suofeiya.com.cn/v/1c283ad3-d8ae-4872-b53d-ed48deb9c4ab",
            "https://file.suofeiya.com.cn/v/0a6252d8-ff56-4ea4-91d8-2cdf54ca8ac9",
            "https://file.suofeiya.com.cn/v/a35a1477-ecc2-4637-8e8d-01372b66d62f",
            "https://file.suofeiya.com.cn/v/e1617fdb-98ef-41d5-aadd-24326227a43f",
            "https://file.suofeiya.com.cn/v/7f73100e-06b7-48a3-a2f4-0edb6d30d856",
            "https://file.suofeiya.com.cn/v/879d34d4-4d58-412c-b8d1-fcb1a04cf7f9",
            "https://file.suofeiya.com.cn/v/329ac269-6387-4434-bf0c-960a487930f7",
        ],
        'cover': "https://file.suofeiya.com.cn/v/ce9c01e4-12e9-49d6-995b-b783a4a0fc94",
        'allow_download': False,
        'who_can_watch': "fans",
        'publish_time': {
            'type': "delay",
            'time': (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M"),
        },
    }
    create_content = CreatorContent(user_id=request.get("user_id"), save_state=True, brower_headless=False, browser_devtools=True, slow_mo=200)
    # 调用发送验证码方法
    response = create_content.upload_image_text(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")

