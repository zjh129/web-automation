import os
import random

from content_tools import settings
from content_tools.helpers import log, utils, download
from content_tools.helpers.common import mq_json_response, validate_phone_number
from content_tools.libary.base import exception
from content_tools.libary.douyin.creator_base import CreatorBase
from content_tools.libary.douyin.models_creator.captcha_page import CaptchaPage
from content_tools.libary.douyin.models_creator.content_login_page import ContentLoginPage
from content_tools.libary.xiaohongshu.exceptions import ApiErrorCode


class CreatorLogin(CreatorBase):
    """
    抖音web登录类，用于登录抖音web端
    """

    login_type_qrcode = "qrcode"  # 二维码登录
    login_type_qrcode_base64 = "qrcode_base64"  # 二维码登录-获取二维码base64
    login_type_phone = "phone"  # 手机号登录
    login_type_phone_send_code = "phone_send_code"  # 手机号发送验证码
    login_type_account = "account"  # 账号密码登录
    login_type_cookie = "cookie"  # cookie登录

    @exception.exception_handler
    def login(self, login_type, request):
        """
        登录
        """
        # 首页元素
        page = ContentLoginPage(self.page)
        # 跳转首页
        page.to_home()
        # 提前检查登录状态，不做无用的登录操作
        if self.check_login_state():
            raise ApiErrorCode(0, "您已登录成功")
        # 点击登录按钮，弹出登录框
        page.btn_login().click()
        # select login type
        if login_type == "qrcode":
            data = self.login_by_qrcode()
        elif login_type == "qrcode_base64":
            data = self.login_by_qrcode_get_qrcode_base64()
        elif login_type == 'phone_send_code':
            data = self.login_by_mobile_send_code(request)
        elif login_type == "phone":
            data = self.login_by_mobile(request)
        elif login_type == "account":
            data = self.login_by_account(request)
        elif login_type == "cookie":
            data = self.login_by_cookies(request)
        else:
            raise ValueError("无效的登录类型")
        return data

    def login_by_mobile_send_code(self, request):
        """
        发送验证码，使用playwright 的python包
        """
        # 返回json
        # 获取手机号码
        phone = request.get("phone", "")
        # 验证手机号码
        self.validate_phone(phone)
        # 初始化页面元素模型
        page = ContentLoginPage(self.page)

        # 标签页切换到验证码登录选项卡
        page.tab_mobile().click()
        # 等待验证码登录框出现
        page.btn_change_to_mobile_code()

        # 等待验证码登录框出现-手机号为中国手机号,暂时不做设置
        # page.input_mobile_area_code().fill("+86")
        # 输入手机号码
        page.input_mobile_mobile_number().fill(phone)
        # 点击发送验证码
        with self.page.expect_response(
                lambda response: "https://sso.douyin.com/send_activation_code/v2/" in response.url) as response_info:
            page.btn_mobile_send_code().click()
        response_json = response_info.value.json()
        # 验证码发送处理，重点处理验证码逻辑
        captcha_page = CaptchaPage(self.page)
        # 短信验证码未发送成功时，最多情况下会发送两次：第一次会弹验证码，第二次就发送成功
        send_verify_times = 2
        send_verify_success = False
        while not send_verify_success:
            if send_verify_times <= 0:
                log.logger.error("发送验证码次数超过上线 ...")
                break
            try:
                if response_json.get("error_code") == 0:
                    send_verify_success = True
                    continue
                # 发送短信验证码接口响应失败，会产生两种结果：
                # 一种是短信发送过于频繁、或其他错误，可能被平台拦截，无法调用接口发送短信验证码，该类响应无需一直等待，直接不用重试
                # 另一种是短信接口的响应会导致弹出验证码，此时需要处理验证码
                captcha_page.box_captcha().wait_for(timeout=1000, state="visible")
                # 验证码弹框出现，未出现超时异常，将会继续往下运行
                # 此时循环监听页面是否弹出验证码弹框
                captcha_verify_success = False
                captcha_verify_times = 3
                while not captcha_verify_success:
                    if captcha_verify_times <= 0:
                        log.logger.error("发送验证码次数超过上线 ...")
                        break
                    try:
                        # 自动检验安全验证码
                        captcha_page.check_captcha()
                    except ApiErrorCode as e:
                        # 该类异常表示程序无需重试，直接抛出异常
                        raise e
                    except Exception as e:
                        log.logger.error(f"验证码发送流程处理异常, error: {e}")
                        continue
                    finally:
                        # 安全验证码验证处理间隔1秒
                        self.page.wait_for_timeout(1000)
                        # 验证码次数减1
                        captcha_verify_times -= 1
                        # 在无人工操作的情况下，验证码弹框在验证成功后自动消失
                        if not captcha_page.box_captcha().is_visible():
                            captcha_verify_success = True
            except ApiErrorCode as e:
                # 该类异常表示程序无需重试，直接抛出异常
                raise e
            except Exception as e:
                log.logger.error(f"验证码发送流程处理异常, error: {e}")
                continue
            finally:
                # 等待1秒后重试
                self.page.wait_for_timeout(1000)
                # 验证码次数减1
                send_verify_times -= 1
                # 在无人工操作的情况下，验证码弹框在验证成功后自动消失
                if not captcha_page.box_captcha().is_visible():
                    send_verify_success = True

        if send_verify_success is True:
            return {"message": "发送验证码成功"}
        elif response_json is None:
            raise ApiErrorCode(ApiErrorCode.CODE_UNKNOWN_ERROR, "发送验证码请求失败")
        elif response_json.get("error_code") != 0:
            # 不存在errorCode参数或不存在errorMsg参数时，使用默认错误码
            error_code = response_json.get("error_code", ApiErrorCode.CODE_UNKNOWN_ERROR)
            error_msg = response_json.get("description", "")
            raise ApiErrorCode(error_code, error_msg)

    def login_by_mobile(self, request):
        """
        发送验证码，使用playwright 的python包
        """
        # 返回json
        # 获取手机号码
        phone = request.get("phone", "")
        # 验证手机号码
        self.validate_phone(phone)
        # 初始化页面元素模型
        page = ContentLoginPage(self.page)

        # 标签页切换到验证码登录选项卡
        page.tab_mobile().click()
        # 等待验证码登录框出现
        page.btn_change_to_mobile_code()
        # 初始化响应json
        response_json = None
        # 等待验证码登录框出现-手机号为中国手机号,暂时不做设置
        # page.input_mobile_area_code().fill("+86")
        # 输入手机号码
        page.input_mobile_mobile_number().fill(phone)
        # 输入手机验证码
        page.input_mobile_verification_code().fill(request.get("code", ""))
        # 勾选同意协议
        page.btn_agreement_check()
        # 点击登录按钮
        with self.page.expect_response(
                lambda response: "https://sso.douyin.com/quick_login/v2/" in response.url,
                timeout=5000) as response_info:
            page.btn_submit_login().click()  # 点击登录
        # 等待一秒
        self.page.wait_for_timeout(1000)
        # 登录成功，页面有跳转，无法捕获登录接口的响应，需要手动判断登录是否成功
        if '/creator-micro/home' in self.page.url:
            # 获取登录用户的数据
            with self.page.expect_response(
                    lambda response: "https://creator.douyin.com/aweme/v1/creator/user/info/" in response.url) as response_info:
                self.page.reload()
            self.page.wait_for_load_state(state="load")
            response_json = response_info.value.json()
            return {"user_profile": response_json.get("user_profile", {}), "message": "登录成功"}
        else:
            response_json = response_info.value.json()

        if response_json is None:
            raise ApiErrorCode(ApiErrorCode.CODE_UNKNOWN_ERROR, "登录失败，未捕获响应")
        elif response_json.get("error_code") != 0:
            # 不存在errorCode参数或不存在errorMsg参数时，使用默认错误码
            error_code = response_json.get("error_code", ApiErrorCode.CODE_UNKNOWN_ERROR)
            error_msg = response_json.get("description", "")
            raise ApiErrorCode(error_code, error_msg)
        return {"message": "登录成功"}

    def validate_phone(self, phone):
        """
        验证手机号码
        phone: 手机号码
        """
        # 如果phone为空，返回错误信息
        if not phone:
            raise ApiErrorCode(ApiErrorCode.CODE_PHONE_NUMBER_EMPTY)

        # 如果phone格式不正确，返回错误信息
        is_valid = validate_phone_number(phone)
        if not is_valid:
            raise ApiErrorCode(ApiErrorCode.CODE_PHONE_INCORRECT)

    def login_by_qrcode(self):
        """
        扫码登录
        """
        # 删除二维码登录结果
        if self.scan_login_qrcode_result_get() is not None:
            log.logger.error("已有扫码流程执行中，无需重复执行 ...")
            return
        # 初始化扫码登录结果
        self.scan_login_qrcode_result_set(login_state=False)
        # 返回json
        scan_qrcode_path = None
        # 初始化页面元素模型
        page = ContentLoginPage(self.page)

        # 标签页切换到验证码登录选项卡
        page.tab_scan_code().click()
        # 等待二维码登录框出现
        wait_times = 5 * 60  # 最长等待5分钟
        # 更新当前用户的扫码图片
        qrcode_replace = True
        # 登录是否成功标识
        login_success = False
        while not login_success:
            if wait_times <= 0:
                log.logger.error("等待扫码超过五分钟，不再等待 ...")
                break
            # 验证登录状态
            if '/creator-micro/home' in self.page.url:
                login_success = True
                break
            try:
                # 如果错误提示框存在，则抛出异常
                # if page.scan_code_error().is_visible():
                #     raise ApiErrorCode(ApiErrorCode.CODE_LOGIN_ERROR, page.msg_box_error().inner_text())
                # 如果刷新按钮存在，则点击刷新按钮
                if page.btn_scan_refresh().is_visible():
                    page.btn_scan_refresh().click()
                    # 更新当前用户的扫码图片
                    qrcode_replace = True
                    page.img_qrcode().wait_for(timeout=1000, state="attached")
                # 保存二维码图片
                scan_qrcode_path = download.save_base64_image(
                    page.img_qrcode().get_attribute("src"),
                    filename=f"{self.user_id}",
                    save_directory=os.path.join(
                        settings.BASE_SCAN_LOGIN_QRCODE_DIR, self.platform),
                    force_replace=qrcode_replace,
                )
                # 更新当前二维码图片的过期状态
                up_qrcode_expired = None
                if qrcode_replace:
                    up_qrcode_expired = True
                # 更新扫码信息
                self.scan_login_qrcode_result_set(
                    qrcode_info={
                        "qrcode_file_path": scan_qrcode_path,
                        "login_desc": page.scan_code_desc().inner_text().replace("\n", "")
                    },
                    qrcode_expired=up_qrcode_expired,
                )
            except ApiErrorCode as e:
                # 该类异常表示程序无需重试，直接抛出异常
                raise e
            except Exception as e:
                log.logger.error(f"扫码登录流程异常, error: {e}")
                continue
            finally:
                # 等待1秒后重试
                self.page.wait_for_timeout(1000)
                # 验证码次数减1
                wait_times -= 1
                # 重置强制替换标识
                qrcode_replace = False

        # 获取登录用户的数据
        with self.page.expect_response(
                lambda response: "https://creator.douyin.com/aweme/v1/creator/user/info/" in response.url) as response_info:
            self.page.reload()
        self.page.wait_for_load_state(state="load")
        response_json = response_info.value.json()

        # 登录操作完成后，删除二维码图片
        if scan_qrcode_path and os.path.exists(scan_qrcode_path):
            os.remove(scan_qrcode_path)

        if login_success is False:
            self.scan_login_qrcode_result_del()
            raise ApiErrorCode(ApiErrorCode.CODE_LOGIN_ERROR, "扫码登录等待到达5分钟，未捕获响应")
        result = {"user_id": self.user_id, "user_profile": response_json.get("user_profile", {})}
        # 将登录结果存储到redis中
        self.scan_login_qrcode_result_set(login_state=True, user_profile=response_json.get("user_profile", {}))
        return result

    def login_by_qrcode_get_qrcode_base64(self):
        """
        扫码登录图片base64获取
        """
        if self.user_id == "":
            raise ApiErrorCode(ApiErrorCode.CODE_USER_ID_EMPTY)

        cache_data = self.scan_login_qrcode_result_get()
        if cache_data is None:
            raise ApiErrorCode(ApiErrorCode.CODE_LOGIN_ERROR, "请先触发扫码登录")
        qrcode_info = cache_data.get("qrcode_info")
        if cache_data is None or qrcode_info is None or qrcode_info.get("qrcode_file_path") is None:
            raise ApiErrorCode(ApiErrorCode.CODE_LOGIN_ERROR, "二维码图片不存在")
        # 如果二维码已经读取过，则将二维码过期的标识删除
        if cache_data.get("qrcode_expired", False) is True:
            self.scan_login_qrcode_result_set(qrcode_expired=False)

        # 将二维码图片转换为base64字符串
        qrcode_base64 = download.image_to_base64(qrcode_info.get("qrcode_file_path"))
        if qrcode_base64 is None:
            raise ApiErrorCode(ApiErrorCode.CODE_LOGIN_ERROR, "二维码图片无效或不存在")
        # 返回二维码图片的base64字符串
        return {"qrcode_base64": qrcode_base64, 'login_desc': qrcode_info.get('login_desc', "")}

    def login_by_account(self, request):
        """
        账号密码登录
        备注：通过账号密码登录，需要通过手机号+手机验证码的方式登录才行
        """
        # 获取手机号码
        phone = request.get("phone", "")
        # 验证手机号码
        self.validate_phone(phone)
        # 验证密码不为空
        password = request.get("password", "")
        if password == "":
            raise ApiErrorCode(ApiErrorCode.CODE_PASSWORD_EMPTY)
        # 初始化页面元素模型
        page = ContentLoginPage(self.page)

        # 标签页切换到验证码登录选项卡
        page.tab_mobile().click()
        # 等待验证码登录框出现
        page.btn_change_to_mobile_password()
        # 等待验证码登录框出现-手机号为中国手机号,暂时不做设置
        # page.input_mobile_area_code().fill("+86")
        # 输入手机号码
        page.input_mobile_mobile_number().fill(phone)
        # 输入密码
        page.input_mobile_password().fill(password)

        # 勾选同意协议
        page.btn_agreement_check()
        # 点击登录按钮
        with self.page.expect_response(
                lambda response: "https://sso.douyin.com/account_login/v2/" in response.url,
                timeout=5000) as response_info:
            # 鼠标悬停
            page.btn_submit_login().hover()
            # 鼠标移动
            bounding_box = page.btn_submit_login().bounding_box()
            self.page.mouse.move(bounding_box["x"] + random.uniform(0, bounding_box["width"]),
                                 bounding_box["y"] + random.uniform(0, bounding_box["height"]))
            # 点击
            page.btn_submit_login().click(button="left")  # 点击登录
        if response_info.value is not None:
            response_json = response_info.value.json()

        if response_json is None:
            raise ApiErrorCode(ApiErrorCode.CODE_UNKNOWN_ERROR, "登录失败，未捕获响应")
        elif response_json.get("error_code") != 0:
            # 不存在errorCode参数或不存在errorMsg参数时，使用默认错误码
            error_code = response_json.get("error_code", ApiErrorCode.CODE_UNKNOWN_ERROR)
            error_msg = response_json.get("description", "")
            raise ApiErrorCode(error_code, error_msg)
        return {"message": "登录成功"}

    def login_by_cookies(self, request):
        log.logger.info("Begin login douyin by cookie ...")
        cookie_str = request.get('cookie_str', '')
        for key, value in utils.convert_str_cookie_to_dict(cookie_str).items():
            self.context.add_cookies([{
                'name': key,
                'value': value,
                'domain': ".douyin.com",
                'path': "/"
            }])
        return {}

    @exception.exception_handler
    def get_login_state(self):
        """
        获取登录状态
        """
        self.page.goto(self.base_url)
        state = self.check_login_state()
        return {"state": state}
