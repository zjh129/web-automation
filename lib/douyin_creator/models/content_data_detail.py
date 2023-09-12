from content_tools.helpers import log
from content_tools.libary.douyin.models.base_page import BasePage
from content_tools.libary.xiaohongshu.exceptions import ApiErrorCode
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from datetime import datetime, timedelta


class ContentDataDetailPage(BasePage):
    """
    创作平台-作品数据详情页-页面操作元素
    """
    def to_home(self, aweme_id):
        """
        跳转到首页
        """
        self.page.goto(f"/creator-micro/data/stats/video/{aweme_id}?enter_from=item_data")
