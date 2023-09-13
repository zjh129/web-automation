import json
import os

from playwright.sync_api import sync_playwright

from configs import settings
from helpers import log, utils,redis
from lib.exceptions import ActionException


class Base:
    """
    抖音基类
    """
    browser_headless = True # 是否使用无头浏览器
    context = None # 上下文
    playwright = None # 浏览器引擎
    browser = None # 浏览器
    page = None # 页面
    save_state = True  # 设置是否保持浏览器状态
    save_state_level = "cookies"  # 保存登录状态的方式，user_data_dir、storage_state、cookies
    browser_devtools = False # 是否开启浏览器开发者工具
    browser_slow_mo = None  # 每一步操作减慢指定毫秒数
    platform = "base"  # 平台名称
    user_id = None # 用户ID，用户区分不同用户之间的浏览器数据
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"  # 用户代理
    base_url = "https://www.douyin.com" # 首页地址

    def __init__(self, **kwargs):
        # 上下文存储路径
        if kwargs.get("context_storage_path") is not None:
            self.context_storage_path = kwargs.get("context_storage_path")
        else:
            self.context_storage_path = os.path.join(settings.BASE_DIR, "storage", "browser", self.platform)
        # 当上下文存储路径不存在时，创建上下文存储路径
        if not os.path.exists(self.context_storage_path):
            os.makedirs(self.context_storage_path)

        # 是否保存浏览器状态
        if kwargs.get("save_state") is not None:
            self.save_state = kwargs.get("save_state")

        # 浏览器状态保存方式
        if kwargs.get("save_state_level") is not None:
            self.save_state_level = kwargs.get("save_state_level")

        # 是否使用无头浏览器
        if kwargs.get("brower_headless") is not None:
            self.browser_headless = kwargs.get("brower_headless")

        # 是否开启浏览器开发者工具
        if kwargs.get("browser_devtools") is not None:
            self.browser_devtools = kwargs.get("browser_devtools")

        # 每一步操作减慢指定毫秒数
        if kwargs.get("slow_mo") is not None:
            self.browser_slow_mo = kwargs.get("slow_mo")

        # 用户代理设置
        if kwargs.get("user_agent") is not None:
            self.user_agent = kwargs.get("user_agent")
        else: # 否则随机切换用户代理
            self.user_agent = utils.get_user_agent()

        # 用户ID
        if kwargs.get("user_id") is not None:
            self.user_id = kwargs.get("user_id")

    def launch_browser(self):
        """
        启动浏览器
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium
        # 初始化上下文
        self.context = self.create_browser_context()
        self.context.add_init_script(path=settings.STEALTH_JS_PATH)
        # 如果当前浏览器有打开标签页，则直接返回第一个标签页
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()
        log.logger.info("Douyin Browser Launch finished ...")

    def create_browser_context(self):
        """
        获取浏览器上下文
        """
        playwright_proxy = self.create_browser_proxy()
        if self.save_state:
            if self.save_state_level == "user_data_dir": # 保存用户数据
                user_data_dir = os.path.join(self.context_storage_path, self.user_id)
                browser_context = self.browser.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    accept_downloads=True,
                    headless=self.browser_headless,
                    proxy=playwright_proxy,  # type: ignore
                    viewport={"width": 1920, "height": 1080},
                    user_agent=self.user_agent,
                    base_url=self.base_url,
                    devtools=self.browser_devtools,
                    slow_mo=self.browser_slow_mo,
                )  # type: ignore
            elif self.save_state_level == "storage_state": # 保存存储目录
                browser = self.browser.launch(headless=self.browser_headless,
                                              proxy=playwright_proxy,
                                              devtools=self.browser_devtools,
                                              slow_mo=self.browser_slow_mo,
                                              )  # type: ignore
                storage_state_path = os.path.join(self.context_storage_path, self.user_id, "storage_state.json")
                # 判断存储状态文件是否存在
                if os.path.exists(storage_state_path):
                    with open(storage_state_path, "r") as f:
                        storage_state = json.load(f)
                else:
                    storage_state = None
                browser_context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=self.user_agent,
                    base_url=self.base_url,
                    storage_state=storage_state,
                )
            elif self.save_state_level == "cookies": # cookies方式保存登录状态
                browser = self.browser.launch(headless=self.browser_headless,
                                              proxy=playwright_proxy,
                                              devtools=self.browser_devtools,
                                              slow_mo=self.browser_slow_mo,
                                              )  # type: ignore
                browser_context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=self.user_agent,
                    base_url=self.base_url,
                )
                storage_cookie_path = os.path.join(self.context_storage_path, self.user_id, "cookies.json")
                if os.path.exists(storage_cookie_path):
                    with open(storage_cookie_path, "r") as f:
                        storage_state = json.load(f)
                    browser_context.add_cookies(storage_state)
            return browser_context
        else:
            browser = self.browser.launch(headless=self.browser_headless,
                                          proxy=playwright_proxy,
                                          devtools=self.browser_devtools,
                                          slow_mo=self.browser_slow_mo,
                                          )  # type: ignore
            browser_context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=self.user_agent,
                base_url=self.base_url,
            )
            return browser_context

    def create_browser_proxy(self):
        """
        创建浏览器代理
        """
        return None
        user_id = self.user_id
        # TODO::待完成
        playwright_proxy = {
            # "server": f"{config.IP_PROXY_PROTOCOL}{ip_proxy}",
            # "username": config.IP_PROXY_USER,
            # "password": config.IP_PROXY_PASSWORD,
        }
        return playwright_proxy

    def scan_login_qrcode_result_get(self):
        """
        获取扫码登录结果
        """
        scan_login_qrcode_result_key = f"scan_login_qrcode_result:{self.platform}:{self.user_id}"
        return redis.redis_manager.get(scan_login_qrcode_result_key)

    def scan_login_qrcode_result_set(self, **kwargs):
        """
        设置扫码登录结果

        Args:
            **kwargs: 关键字参数，包含以下参数：
                - qrcode_info (dict, optional): 扫码信息，默认为空字典
                - qrcode_expired (bool, optional): 扫码是否过期，默认为False
                - login_result (bool, optional): 登录结果，默认为空
                - user_profile (dict, optional): 用户信息，默认为空字典

        Returns:
            bool: 设置结果，设置成功返回True，否则返回False

        """
        data = self.scan_login_qrcode_result_get()
        if data is None:
            data = {
                "qrcode_info": kwargs.get("qrcode_info", {}),
                "qrcode_expired": False,
                "login_state": False,
                "user_profile": {},
            }
        if kwargs.get("qrcode_info") is not None:
            data["qrcode_info"] = kwargs.get("qrcode_info")
        if kwargs.get("qrcode_expired") is not None:
            data["qrcode_expired"] = kwargs.get("qrcode_expired")
        if kwargs.get("login_state") is not None:
            data["login_state"] = kwargs.get("login_state")
        if kwargs.get("user_profile") is not None:
            data["user_profile"] = kwargs.get("user_profile")
        scan_login_qrcode_result_key = f"scan_login_qrcode_result:{self.platform}:{self.user_id}"
        return redis.redis_manager.set(scan_login_qrcode_result_key, data, ex=60 * 5)

    def scan_login_qrcode_result_del(self):
        """
        删除扫码登录结果
        """
        scan_login_qrcode_result_key = f"scan_login_qrcode_result:{self.platform}:{self.user_id}"
        return redis.redis_manager.delete(scan_login_qrcode_result_key)

    def close(self):
        """
        析构函数，关闭page、browser和playwright
        """
        try:
            # 保存登录状态
            if self.save_state:
                if self.save_state_level == "storage_state": # 保存存储目录
                    storage_state_path = os.path.join(self.context_storage_path, self.user_id, "storage_state.json")
                    if not os.path.exists(os.path.dirname(storage_state_path)):
                        os.makedirs(os.path.dirname(storage_state_path))
                    self.context.storage_state(path=storage_state_path)
                if self.save_state_level == "cookies": # cookies方式保存登录状态
                    storage_cookie_path = os.path.join(self.context_storage_path, self.user_id, "cookies.json")
                    if not os.path.exists(os.path.dirname(storage_cookie_path)):
                        os.makedirs(os.path.dirname(storage_cookie_path))
                    cookies = self.context.cookies()
                    with open(storage_cookie_path, "w") as f:
                        json.dump(cookies, f)
            if self.page is not None:
                self.page.close()
            # if self.browser is not None:
            #     self.browser.close()
            if self.context is not None:
                self.context.close()
            if self.playwright is not None:
                self.playwright.stop()
        except Exception as e:
            log.logger.error(f"回收浏览器资源失败：{e}", exc_info=True)

    def __enter__(self):
        if self.user_id == "" or self.user_id is None:
            raise ActionException(ActionException.CODE_USER_ID_EMPTY)
        # 启动浏览器
        self.launch_browser()
        """
        上下文管理器，返回self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器，关闭浏览器
        """
        self.close()
