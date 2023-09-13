from helpers import log
from lib.douyin_creator.login import CreatorLogin
from tests import test_env_config


def test_login_by_mobile_send_code():
    """手机号码格式正确,发送验证码成功"""
    request = {'user_id': test_env_config["douyin"]["user_id"], 'phone': test_env_config["douyin"]["phone"]}
    with CreatorLogin(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_phone_send_code, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")


def test_login_by_mobile():
    """手机号码格式正确,发送验证码成功"""
    # 模拟请求参数
    request = {'user_id': test_env_config["douyin"]["user_id"], 'phone': test_env_config["douyin"]["phone"],
               'code': test_env_config["douyin"]["code"]}
    with CreatorLogin(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_phone, request)
    log.logger.info(response)
    print(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_qrcode():
    request = {'user_id': test_env_config["douyin"]["user_id"]}
    with CreatorLogin(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_qrcode, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_qrcode_get_qrcode_base64():
    request = {'user_id': test_env_config["douyin"]["user_id"]}
    with CreatorLogin(user_id=request.get('user_id')) as login:
        # 调用发送验证码方法
        response = login.login_by_qrcode_get_qrcode_base64()
    assert response.get("code") == 0
    assert "成功" in response.get("message")
    assert response.get("data", {}).get("qrcode_base64", "") != ""
    print(response)


def test_scan_login_qrcode_result_get():
    request = {'user_id': test_env_config["douyin"]["user_id"]}
    with CreatorLogin(user_id=request.get("user_id")) as login:
        # 调用发送验证码方法
        response = login.scan_login_qrcode_result_get()
    print(response)
    assert response is not None
    print(response)


def test_login_by_account():
    request = {'user_id': test_env_config["douyin"]["user_id"], "phone": test_env_config["douyin"]["phone"],
               "password": test_env_config["douyin"]["password"]}
    with CreatorLogin(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_account, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_state():
    request = {'user_id': test_env_config["douyin"]["user_id"], 'phone': test_env_config["douyin"]["phone"]}
    with CreatorLogin(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as login:
        response = login.get_login_state()
    assert response.get("code") == 0
    assert response.get("data", {}).get("state") == True
