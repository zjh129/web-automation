from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from datetime import datetime, timedelta

from helpers import log
from lib.base_page import BasePage
from lib.exceptions import ActionException


class ContentUploadImageTextPage(BasePage):
    """
    创作平台-作品发布-页面元素、基础操作
    """
    who_can_watch_list = {
        "all": "所有人",
        "fans": "好友可见",
        "private": "仅自己可见",
    }
    release_time_list = {
        "now": "立即发布",
        "delay": "定时发布",
    }

    def to_home(self):
        """
        跳转到首页
        """
        self.page.goto("/creator-micro/content/upload?default-tab=3")

    def tab_video(self):
        """
        发布视频标签页
        """
        return self.page.locator(
            'xpath=//div[contains(@class, "card-container-creator-layout")]//div[text()="发布视频"]')

    def tab_image_text(self):
        """
        发布图文标签页
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[text()="发布图文"]')

    def tab_panoramic_video(self):
        """
        发布全景视频标签页
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[text()="发布全景视频"]')
    def btn_upload(self):
        """
        上传按钮
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class, "upload") and descendant::text()[contains(., "图片")]]')

    def set_upload_image(self, image_list):
        """
        上传图片
        """
        self.page.wait_for_load_state("domcontentloaded")
        selector = 'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class, "upload") and descendant::text()[contains(., "图片")]]'
        locator = self.page.locator(selector)
        with self.page.expect_file_chooser() as fc_info:
            bounding = locator.bounding_box()
            self.page.mouse.click(bounding["x"] + bounding["width"] / 2, bounding["y"] + bounding["height"] / 2)

        fc_info.value.set_files(image_list)

    def btn_re_upload(self):
        """
        重新上传按钮
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class, "phone-container")]//button[span[contains(text(), "重新上传")]]')

    def toast(self):
        """
        提示框
        """
        return self.page.locator(
            'xpath=//div[contains(@class, "semi-toast-wrapper")]/div[contains(@class, "semi-toast-warning") or contains(@class, "semi-toast-error")]')

    def set_cover(self, image_path):
        """
        设置封面

        Args:
            image_path (str): 封面图片路径

        """
        upload_btn_selector = 'xpath=//div[contains(@class, "card-container-creator-layout")]//div[text() = "封面设置"]/following-sibling::div[1]//span[span[text()="编辑封面"]]'
        # 点击选择封面按钮
        self.page.locator(upload_btn_selector).click()
        # 切换封面上传标签页
        upload_box_selector = 'xpath=//div[text()="设置封面"]/following-sibling::div[1]'
        # 等待上传框显示
        self.page.locator(upload_box_selector).wait_for(state="visible")
        # 切换手动上传封面标签
        self.page.locator(upload_box_selector + '//div[@role="tab" and text()="上传封面"]').click()
        # 等待上传触发区域显示
        trigger_selector = upload_box_selector + '//label[contains(@class,"upload-btn")]'
        # 显示上传触发区域
        self.page.locator(trigger_selector).wait_for(state="visible")
        # 上传封面图片
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(trigger_selector).click()

        fc_info.value.set_files(image_path)
        # 裁切封面
        cut_selector = 'xpath=//div[text()="裁剪封面"]'
        # 预览封面
        cut_preview_selector = cut_selector + '/following-sibling::div[contains(@class, "cover-cut")]//div[contains(@class, "cover-preview__img")]/img'
        self.page.locator(cut_preview_selector).wait_for(state="visible")
        # 点击裁切确认按钮
        cut_ok_selector = cut_selector + '/following-sibling::div[contains(@class, "dialog-operation")]/button[text()="确定"]'
        self.page.locator(cut_ok_selector).click()
        self.page.wait_for_load_state("domcontentloaded")
        # 检查裁切操作是否有提示
        toast = self.toast()
        try:
            toast.wait_for(timeout=1000, state="visible")
            toast_text = toast.inner_text()
            if toast.is_visible() and toast_text != "":
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_COVER_UPLOAD_ERROR,
                                   "上传封面失败,错误内容为：" + toast_text)
        except ActionException as e:
            raise e
        except PlaywrightTimeoutError as e:
            log.logger.error("提示框不出现，继续执行", exc_info=True)
        except Exception as e:
            log.logger.error(e, exc_info=True)
            raise e

        # 完成按钮
        ok_btn = self.page.locator(
            upload_box_selector + '//div[contains(@class, "operation")]//button[text()="确定"]')
        # 等待”完成“按钮激活
        self.page.wait_for_timeout(1500)
        # ok_btn.wait_for(state="visible")
        # 点击完成按钮
        ok_btn.click()
        # 等待上传框隐藏
        try:
            toast.wait_for(timeout=1000, state="visible")
            toast_text = toast.inner_text()
            if toast.is_visible() and toast_text != "":
                raise ActionException(ActionException.CODE_DOUYIN_VIDEO_COVER_UPLOAD_ERROR,
                                   "上传封面失败,错误内容为：" + toast_text)
        except ActionException as e:
            raise e
        except PlaywrightTimeoutError as e:
            log.logger.error("提示框不出现，继续执行", exc_info=True)
        except Exception as e:
            log.logger.error(e, exc_info=True)
            raise e
        self.page.locator(upload_box_selector).wait_for(timeout=120000, state="detached")


    def text_title(self):
        """
        作品标题
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//input[contains(@placeholder, "添加作品标题")]')

    def text_description(self):
        """
        作品描述
        """
        return self.page.locator(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class, "zone-container") and contains(@data-placeholder, "作品描述")]')

    def set_download_image(self, is_checked=False):
        """
        允许他人保存图片

        Args:
            is_checked (bool, optional): 是否允许他人保存视频，默认为False

        """

        if not is_checked:
            selector = 'xpath=//div[contains(@class,"card-container-creator-layout")]//div[text()="允许他人保存图片"]/following-sibling::div[1]/div'
            label_allow = self.page.locator(selector + '/label[span[text()="允许"]]')
            label_disallow = self.page.locator(selector + '/label[span[text()="不允许"]]')
            if is_checked is True:
                # 允许他人保存视频
                label_allow.click()
            elif is_checked is False:
                # 不允许他人保存视频
                label_disallow.click()

    def set_who_can_watch(self, type):
        """
        设置谁可以观看

        Args:
            type (str): 观看权限类型，可选值为 "all"（公开）、"fans"（好友可见）、"private"（仅自己可见）

        Raises:
            Exception: 如果参数错误，则抛出异常

        """
        if type not in self.who_can_watch_list.keys():
            raise Exception("参数错误")
        selector = 'xpath=//div[contains(@class,"card-container-creator-layout")]//div[text()="设置谁可以看"]/following-sibling::div[1]/div'
        label_public = self.page.locator(selector + '/label[span[text()="公开"]]')
        label_friends = self.page.locator(selector + '/label[span[text()="好友可见"]]')
        label_private = self.page.locator(selector + '/label[span[text()="仅自己可见"]]')
        if type == "all":
            # 设置为公开可见
            label_public.click()
        elif type == "fans":
            # 设置为好友可见
            label_friends.click()
        elif type == "private":
            # 设置为仅自己可见
            label_private.click()

    def set_publish_time(self, settings):
        """
        设置发布时间

        Args:
            settings (Settings): 发布时间设置对象，包含以下属性：
                - type (str): 发布时间类型，可选值为 "now" 或 "delay"
                - time (str): 定时发布的时间，格式为字符串，例如 "2022-01-01 12:00"

        Raises:
            Exception: 如果参数错误，则抛出异常

        """
        if settings.get("type") not in self.release_time_list.keys():
            raise Exception("参数错误")
        selector = 'xpath=//div[contains(@class,"card-container-creator-layout")]//div[text()="发布时间"]/following-sibling::div[1]/div'
        if settings.get("type") == "now":
            self.page.locator(selector + '/label[span[text()="立即发布"]]').click()
        elif settings.get("type") == "delay":
            self.page.locator(selector + '//label[span[text()="定时发布"]]').click()
            # 设置定时发布时间
            if settings.get("time", "") == "":
                raise ActionException(ActionException.CODE_PARAM_MISSING,
                                   "发布时间不能为空")
            input_time = datetime.strptime(settings.get("time"), '%Y-%m-%d %H:%M')
            now = datetime.now()
            if input_time < now - timedelta(hours=2) or input_time > now + timedelta(days=14):
                raise ActionException(ActionException.CODE_DOUYIN_PUBLISH_TIME_ERROR,
                                   "发布时间必须在当前时间前后2小时或14天内")
            self.page.locator(selector + '//div[contains(@class, "date-picker")]//input').fill(settings.get("time"))

    def btn_publish(self):
        """
        发布按钮
        """
        return self.page.wait_for_selector(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class,"content-confirm-container")]//button[text()="发布"]')

    def btn_cancel(self):
        """
        取消按钮
        """
        return self.page.wait_for_selector(
            'xpath=//div[contains(@class,"card-container-creator-layout")]//div[contains(@class,"content-confirm-container")]//button[text()="取消"]')
