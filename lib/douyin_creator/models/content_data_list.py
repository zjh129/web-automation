from lib.base_page import BasePage


class ContentDataListPage(BasePage):
    """
    创作平台-作品数据详情页-页面操作元素
    """
    def to_home(self):
        """
        跳转到首页
        """
        self.page.goto("/creator-micro/data/stats/video")
