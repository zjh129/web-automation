from content_tools.helpers import log
from content_tools.libary.douyin.creator_login import CreatorLogin


def test_login_by_mobile_send_code():
    """手机号码格式正确,发送验证码成功"""
    # request = {'user_id': '19106013803', 'phone': '19106013803'}
    request = {'user_id': '18520396239', 'phone': '18520396239'}
    with CreatorLogin(user_id=request.get('user_id'), save_state=True, brower_headless=False,
                      browser_devtools=False, slow_mo=200, save_state_level="storage_state") as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_phone_send_code, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_mobile():
    """手机号码格式正确,发送验证码成功"""
    # 模拟请求参数
    request = {'user_id': '18520396239', 'phone': '18520396239', 'code': "402363"}
    # request = {'user_id': '19106013803', 'phone': '19106013803', 'code': "663340"}
    with CreatorLogin(user_id=request.get('user_id'), save_state=True, brower_headless=False,
                      browser_devtools=False, slow_mo=200, save_state_level="storage_state") as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_phone, request)
    log.logger.info(response)
    print(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_mobile_setcode():
    """
    设置手机号验证码
    """
    login = CreatorLogin()
    # phone = 18520396239
    # phone = 13560187893
    # phone = 17679079107
    phone = 19106013803
    code = '059597'
    login.mobile_code_set(phone, code)
    log.logger.error("test")
    assert login.mobile_code_get(phone) == str(code)


def test_login_by_qrcode():
    request = {'user_id': '19106013803'}
    with CreatorLogin(user_id=request.get('user_id'), save_state=False, brower_headless=False,
                      browser_devtools=False, slow_mo=200) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_qrcode, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_qrcode_get_qrcode_base64():
    request = {'user_id': '19106013803'}
    with CreatorLogin(user_id=request.get('user_id')) as login:
        # 调用发送验证码方法
        response = login.login_by_qrcode_get_qrcode_base64()
    assert response.get("code") == 0
    assert "成功" in response.get("message")
    assert response.get("data", {}).get("qrcode_base64", "") != ""
    print(response)


def test_scan_login_qrcode_result_get():
    request = {'user_id': '19106013803'}
    with CreatorLogin(user_id=request.get("user_id")) as login:
        # 调用发送验证码方法
        response = login.scan_login_qrcode_result_get()
    print(response)
    assert response is not None
    print(response)


def test_login_by_account():
    request = {'user_id': '18520396239', "phone": "18520396239", "password": "123456"}
    with CreatorLogin(user_id=request.get('user_id'), save_state=True, brower_headless=False,
                      browser_devtools=False, slow_mo=200) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_account, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_state():
    request = {'user_id': '18520396239', 'phone': '18520396239'}
    with CreatorLogin(user_id=request.get('user_id'), save_state=True, brower_headless=False,
                      browser_devtools=False, slow_mo=200) as login:
        response = login.get_login_state()
    assert response.get("code") == 0
    assert response.get("data", {}).get("state") == True
