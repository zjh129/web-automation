from libary.base_page import BasePage


class ContentLoginPage(BasePage):
    """
    创作平台-登录页-页面元素、基础操作
    """

    def to_home(self):
        """
        跳转到首页
        """
        self.page.goto("/")

    def btn_login(self):
        """
        登录按钮
        """
        return self.page.locator(
            'xpath=//header[contains(@class, "creator-header")]//span[@class="login" and text()="登录"]')

    def dialog_model(self):
        """
        弹层元素
        """
        return self.page.wait_for_selector('xpath=//div[@class="semi-portal"]',
                                           state="attached", timeout=1000 * 10)

    def dialog_login(self):
        """
        登录弹框-需等待页面自动弹出
        """
        return self.page.wait_for_selector('xpath=//div[@class="semi-portal"]//div[@class="account-modal"]',
                                           state="attached", timeout=1000 * 10)

    def tab_scan_code(self):
        """
        扫码登录选项卡
        """
        return self.page.locator('xpath=//div[@role="tab-list"]//div[@role="tab" and text()="扫码登录"]')

    def tab_mobile(self):
        """
        验证码登录选项卡
        """
        return self.page.locator('xpath=//div[@role="tab-list"]//div[@role="tab" and text()="手机号登录"]')

    def btn_mobile_code_toggle(self):
        """
        手机登录方式切换按钮
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//div[@class="toggle"]//span')

    def btn_change_to_mobile_code(self):
        """
        切换为验证码登录
        """
        text = self.btn_mobile_code_toggle().inner_text()
        if "验证码登录" in text:
            self.btn_mobile_code_toggle().click()

    def btn_change_to_mobile_password(self):
        """
        切换为密码登录
        """
        text = self.btn_mobile_code_toggle().inner_text()
        if "密码登录" in text:
            self.btn_mobile_code_toggle().click()

    def input_mobile_area_code(self):
        """
        手机号码区号输入框
        """
        return self.page.locator(
            'xpath=//form[contains(@class, "account-phone")]//span[@class="semi-select-selection-text"]')

    def input_mobile_mobile_number(self):
        """
        手机号码输入框
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//input[@placeholder="请输入手机号"]')

    def btn_mobile_send_code(self):
        """
        手机号码发送验证码按钮
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//span[text()="发送验证码"]')

    def input_mobile_verification_code(self):
        """
        手机验证码输入框
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//input[@placeholder="请输入验证码"]')

    def input_mobile_password(self):
        """
        手机密码输入框
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//input[@placeholder="请输入密码"]')

    def btn_agreement_check(self):
        """
        同意协议勾选框
        """
        img = self.page.locator('xpath=//form[contains(@class, "account-phone")]//div[@class="agreement"]/img')
        if 'uncheck' in img.get_attribute("src"):
            img.click()

    def msg_box_error(self):
        """
        错误信息弹框
        """
        return self.page.wait_for_selector('xpath=//form[contains(@class, "account-phone")]//p[@class="err"]',
                                           state="visible", timeout=1000)

    def btn_submit_login(self):
        """
        登录按钮
        """
        return self.page.locator('xpath=//form[contains(@class, "account-phone")]//button[@type="submit"]')

    def img_qrcode(self):
        """
        扫码登录二维码
        """
        return self.page.locator('xpath=//div[@class="semi-portal"]//div[@class="qrcode-image"]/img[1]')

    def scan_code_desc(self):
        """
        扫码登录描述
        """
        return self.page.locator('xpath=//div[@class="semi-portal"]//div[@class="account-qrcode"]//div[@class="account-qrcode-desc"]')

    def scan_code_error(self):
        """
        扫码错误提示
        """
        return self.page.locator('xpath=//div[@class="semi-portal"]//div[@class="account-qrcode"]//p[@class="error"]')

    def btn_scan_refresh(self):
        """
        扫码刷新按钮
        """
        return self.page.locator('xpath=//div[@class="semi-portal"]//div[@class="qrcode-image"]//div//img')
