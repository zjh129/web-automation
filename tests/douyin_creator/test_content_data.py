from helpers import log
from lib.douyin_creator.content import CreatorContent
from tests import test_env_config


def test_get_data_list():
    """
    测试作品列表统计数据
    """
    request = {
        'user_id': test_env_config["douyin"]["user_id"],
    }
    with CreatorContent(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as create_content:
        # 调用发送验证码方法
        response = create_content.get_data_list(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")


def test_get_data_detail():
    """
    测试数据详情方法
    """
    request = {
        'user_id': test_env_config["douyin"]["user_id"],
        'aweme_id': test_env_config["douyin"]["content"]["aweme_id"],
    }
    with CreatorContent(
            user_id=request.get('user_id'),
            save_state=test_env_config["browser"]['save_state'],
            brower_headless=test_env_config["browser"]['headless'],
            browser_devtools=test_env_config["browser"]['browser_devtools'],
            slow_mo=test_env_config["browser"]['slow_mo'],
            save_state_level=test_env_config["browser"]['save_state_level']
    ) as create_content:
        # 调用发送验证码方法
        response = create_content.get_data_detail(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")
