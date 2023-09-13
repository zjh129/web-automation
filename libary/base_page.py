from playwright.sync_api import Page


# BasePage类，所有页面类的基类
class BasePage(object):
    """
    基本页面类
    """

    def __init__(self, page: Page):
        self.page = page

    def getPage(self):  # -> Page
        """
        获取page对象
        """
        return self.page

    def box_captcha(self):
        """
        验证码容器
        """
        return self.page.locator('xpath=//*[@id="captcha_container"]')
