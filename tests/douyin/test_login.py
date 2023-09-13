

def test_login_by_mobile():
    """手机号码格式正确,发送验证码成功"""
    # 模拟请求参数
    # request = {'phone': '19106013803'}
    request = {'user_id': '18520396239','phone': '18520396239'}
    with Login(brower_headless=False, browser_devtools=False, slow_mo=200) as login:
        # 调用发送验证码方法
        response = login.login(login.login_type_phone, request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "登录成功" in response.get("message")


def test_login_by_mobile_setcode():
    """
    设置手机号验证码
    """
    login = Login()
    phone = 18520396239
    code = 932147
    login.mobile_code_set(phone, code)
    log.logger.error("test")
    assert login.mobile_code_get(phone) == str(code)