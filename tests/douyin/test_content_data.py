from content_tools.helpers import log
from content_tools.libary.douyin.creator_content import CreatorContent
from jobs.logic import distribute


def test_get_data_list():
    """
    测试作品列表统计数据
    """
    request = {
        'user_id': '18520396239',
    }
    with CreatorContent(user_id=request.get("user_id"), save_state=True, brower_headless=False, browser_devtools=False, slow_mo=200) as create_content:
        # 调用发送验证码方法
        response = create_content.get_data_list(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")


def test_get_data_list_by_queue():
    """
    测试数据详情方法-队列方式
    """
    request = {
        'user_id': '18520396239',
    }
    distribute.logical_call("dy", "data_list", request_data=request)


def test_get_data_detail():
    """
    测试数据详情方法
    """
    request = {
        'user_id': '18520396239',
        'aweme_id': "7275701688504241423",
    }
    with CreatorContent(user_id=request.get("user_id"), save_state=True, brower_headless=False, browser_devtools=False,
                        slow_mo=200) as create_content:
        # 调用发送验证码方法
        response = create_content.get_data_detail(request)
    log.logger.info(response)
    # 校验返回结果
    assert response.get("code") == 0
    assert "成功" in response.get("message")


def test_get_data_detail_by_queue():
    """
    测试数据详情方法-队列方式
    """
    request = {
        'user_id': '18520396239',
        'aweme_id': "7275701688504241423",
    }
    distribute.logical_call("dy", "data_detail", request_data=request)
