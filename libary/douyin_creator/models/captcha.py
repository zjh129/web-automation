import os
import random
from datetime import datetime

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from configs import settings
from helpers import log, utils
from helpers.verify import factory
from libary.base_page import BasePage
from libary.exceptions import ActionException


class CaptchaPage(BasePage):
    captcha_slider = "slider"  # 滑块验证码类别
    captcha_same_shape = "same_shape"  # 点击两个相同形状的物体

    def captcha_type(self):
        """
        获取验证码类型
        """
        selector = self.box_captcha()
        if selector:
            text = selector.inner_text()
            if "按住左边按钮拖动完成上方拼图" in text:
                return self.captcha_slider
            elif "点击两个形状相同的物体" in text:
                return self.captcha_same_shape
        return None

    """
    验证码弹框
    """

    def box_captcha(self):
        """
        验证码容器
        """
        selector = 'xpath=//*[@id="verify-bar-box"]'
        return self.page.locator(selector)

    def btn_captcha_close(self):
        """
        验证码容器-关闭按钮
        """
        return self.page.locator('xpath=//*[@id="verify-bar-box"]//a[@id="verify-bar-close"]')

    def check_captcha(self):
        """
        验证码检查
        """
        # 如果页面重定向到滑动验证码页面，需要再次滑动滑块
        current_page_title = self.page.title()
        captcha_type = self.captcha_type()
        # 验证码中间页自动验证
        if "验证码中间页" in current_page_title:
            if captcha_type == self.captcha_slider:
                # 滑块验证码
                self.check_page_display_slider(move_step=3, slider_level="hard")
            elif captcha_type == self.captcha_same_shape:
                # 点击两个相同形状的物体
                self.check_same_shape()
        else:
            # 其他弹窗验证码
            if captcha_type == self.captcha_slider:
                # 滑块验证码
                self.check_page_display_slider(move_step=10, slider_level="easy")
            elif captcha_type == self.captcha_same_shape:
                # 点击两个相同形状的物体
                self.check_same_shape()

    def check_page_display_slider(self, move_step: int = 10, slider_level: str = "easy"):
        """
        检查页面是否出现滑动验证码
        :return:
        """
        # 滑动验证码的背景图元素
        back_selector = 'xpath=//div[@class="validate-main"]//img[@id="validate-big"]'
        # 等待滑块验证码出现
        try:
            self.page.wait_for_selector(selector=back_selector, state="visible", timeout=5 * 1000)
        except PlaywrightTimeoutError:  # 没有滑动验证码，直接返回
            return
        gap_selector = 'xpath=//div[@class="validate-main"]//img[@id="validate-big"]//following-sibling::img'
        max_slider_try_times = 3
        slider_verify_success = False
        while not slider_verify_success:
            if max_slider_try_times <= 0:
                log.logger.error("slider verify failed ...")
                break
            try:
                self.move_slider(back_selector, gap_selector, move_step, slider_level)
            except ActionException as e:
                # 该类异常表示程序无需重试，直接抛出异常
                raise e
            except Exception as e:
                log.logger.error(f"滑块验证码验证失败, error: {e}")
                continue
            finally:
                # 如果滑块验证码小时，表示验证成功
                self.page.wait_for_timeout(timeout=1000)
                # 滑块验证码消失则表示成功
                if not self.page.locator(back_selector).is_visible():
                    slider_verify_success = True

                max_slider_try_times -= 1
                log.logger.info(f"滑块验证码验证剩余次数: {max_slider_try_times}")

    def move_slider(self, back_selector: str, gap_selector: str, move_step: int = 10, slider_level="easy"):
        """
        Move the slider to the right to complete the verification
        :param back_selector: 滑动验证码背景图片的选择器
        :param gap_selector:  滑动验证码的滑块选择器
        :param move_step: 是控制单次移动速度的比例是1/10 默认是1 相当于 传入的这个距离不管多远0.1秒钟移动完 越大越慢
        :param slider_level: 滑块难度 easy hard,分别对应手机验证码的滑块和验证码中间的滑块
        :return:
        """

        # get slider background image
        slider_back_elements = self.page.wait_for_selector(
            selector=back_selector,
            timeout=1000 * 10,  # wait 10 seconds
        )
        slide_back = str(slider_back_elements.get_property("src"))  # type: ignore

        # get slider gap image
        gap_elements = self.page.wait_for_selector(
            selector=gap_selector,
            timeout=1000 * 10,  # wait 10 seconds
        )
        gap_src = str(gap_elements.get_property("src"))  # type: ignore

        # 调用验证码识别工厂验证滑块位置
        res = factory.create_verify(factory.VERIFY_TYPE_DDDDOCR).slide(
            gap_image_path=gap_src,
            bg_image_path=slide_back,
        )
        distance = res['x']
        # 获取移动轨迹
        tracks = utils.get_tracks(distance, slider_level)
        new_1 = tracks[-1] - (sum(tracks) - distance)
        tracks.pop()
        tracks.append(new_1)

        # 根据轨迹拖拽滑块到指定位置
        element = self.page.locator('xpath=//div[@class="validate-drag-button"]//img')
        bounding_box = element.bounding_box()  # type: ignore

        self.page.mouse.move(bounding_box["x"] + bounding_box["width"] / 2,  # type: ignore
                             bounding_box["y"] + bounding_box["height"] / 2)  # type: ignore
        # 这里获取到x坐标中心点位置
        x = float(bounding_box["x"] + bounding_box["width"] / 2)  # type: ignore
        y = float(bounding_box["y"] + bounding_box["height"] / 2)  # type: ignore
        # 模拟滑动操作
        # element.hover()  # type: ignore
        self.page.mouse.down()
        trackSum = 0
        for track in tracks:
            # 增加一个随机的Y坐标，模拟人为抖动,通过更改此值，来重现滑块失败弹出点选相同形状验证码
            slide_y = y + random.uniform(1, 5)
            # slide_y = 0
            # 循环鼠标按照轨迹移动
            # steps 是控制单次移动速度的比例是1/10 默认是1 相当于 传入的这个距离不管多远0.1秒钟移动完 越大越慢
            steps_times = int(random.uniform(1, 10))
            if trackSum > distance:
                # 增加一个随机速度，模拟人为抖动
                self.page.mouse.move(bounding_box["x"] + bounding_box["width"] / 2 + distance, slide_y,
                                     steps=steps_times)
                break
            else:
                # 增加一个随机速度，模拟人为抖动
                self.page.mouse.move(x + track, slide_y, steps=steps_times)
            x += track
            trackSum += track
        self.page.mouse.up()

    def check_same_shape(self):
        """
        检查页面是否出现点击两个相同形状的物体验证码
        """
        # 验证码图片选择器
        img_selector = 'xpath=//div[@id="verify-bar-box"]//canvas[@id="verify-canvas"]'
        # 验证结果提示文字
        alert_selector = 'xpath=//div[@id="verify-bar-box"]//div[contains(@class, "valid-text")]'
        # 刷新按钮选择器
        refresh_selector = 'xpath=//div[@id="verify-bar-box"]//button[@id="button-refresh"]'
        # 提交按钮选择器
        submit_selector = 'xpath=//div[@id="verify-bar-box"]//button[@id="button-submit"]'
        max_try_times = 3
        verify_success = False
        while not verify_success:
            if max_try_times <= 0:
                log.logger.error("slider verify failed ...")
                self.page.locator(refresh_selector).click()
                break
            try:
                # 验证码元素
                element = self.page.locator(img_selector)
                # 捕获验证码图片路径,为了能捕获到图片路径，需要先点击一下刷新按钮
                with self.page.expect_response(lambda response: "captcha-sign.bytetos.com/captcha-dl-chn/3d" in response.url,
                        timeout=3000) as response_info:
                    self.page.locator(refresh_selector).click()
                response = response_info.value
                if response.url != "":
                    image_path = response.url
                else:
                    # 捕获不到的情况下截屏
                    image_path = os.path.join(settings.BASE_CLICK_SAME_SHAPE_DIR,
                                              datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".jpg")
                    # 截图前确保没有上次验证结果提示信息
                    self.page.locator(alert_selector).wait_for(timeout=1000, state="hidden")
                    # 截图保存图片
                    element.screenshot(type="jpeg", path=image_path)
                # 通过调接口识别二维码位置
                try:
                    log.logger.info("调用云码解码平台解密验证码坐标")
                    verify_rs = factory.create_verify(factory.VERIFY_TYPE_YDM).same_shape(image_path=image_path, resize=(268, 150))
                except Exception as e:
                    log.logger.error(f"验证码解码服务失败, error: {e}")
                    raise ActionException(ActionException.CODE_VERIFY_SERVICE_ERROR, f"验证码解码服务失败, error: {e}")
                bounding_box = element.bounding_box()  # type: ignore
                # 点击标识位置
                for item in verify_rs:
                    x = float(bounding_box["x"] + item["x"])
                    y = float(bounding_box["y"] + item["y"])
                    self.page.mouse.click(x, y)

                # 提交验证
                with self.page.expect_response(
                        lambda response: "https://verify.snssdk.com/verify" in response.url,
                        timeout=1000) as response_info:
                    self.page.locator(submit_selector).click()
                    response_json = response_info.value.json()
                    if response_json.get("msg_type") != 'success':
                        log.logger.info("check same shape verify failed, retry ...")
                        continue
                    else:
                        verify_success = True
            except ActionException as e:
                # 该类异常表示程序无需重试，直接抛出异常
                raise e
            except Exception as e:
                log.logger.error(f"check same shape failed, error: {e}")
                continue
            finally:
                max_try_times -= 1
                log.logger.info(f"识别相同形状验证码重试剩余次数: {max_try_times}")
                # 点击验证失败，刷新验证码
                if "validate-fail" in self.page.locator(alert_selector).get_attribute("class"):
                    # 验证过于频繁，直接退出整个验证程序
                    alert_text = self.page.locator(alert_selector).inner_text()
                    if "验证过于频繁" in alert_text:
                        raise ActionException(ActionException.CODE_VERIFY_TOO_MANY_TIMES, alert_text)
                # 等待1秒再操作
                self.page.wait_for_timeout(1000)
