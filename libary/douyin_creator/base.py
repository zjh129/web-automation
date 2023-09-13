from helpers import utils
from libary.base import Base


class CreatorBase(Base):
    """
    抖音创作服务平台基础类
    """
    base_url = "https://creator.douyin.com"
    platform = "douyin_creator"

    def check_login_state(self):
        """
        检查登录状态
        """
        self.page.wait_for_load_state("load")
        if self.page.url != f'{self.base_url}/':
            return True
        # 检查是否登录成功
        current_cookie = self.context.cookies()
        _, cookie_dict = utils.convert_cookies(current_cookie)
        if cookie_dict.get("LOGIN_STATUS") == "1":
            return True
        return False