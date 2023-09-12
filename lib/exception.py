from content_tools.helpers import log
from content_tools.helpers.common import mq_json_response
from content_tools.libary.xiaohongshu.exceptions import ApiErrorCode


def exception_handler(func):
    """
    异常处理装饰器
    """
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return mq_json_response(message="执行成功", data=data)
        except ApiErrorCode as e:
            return mq_json_response(code=e.code, message=e.message)
        except Exception as e:
            log.logger.error(f"执行异常：{str(e)}", exc_info=True)
            return mq_json_response(code=ApiErrorCode.CODE_UNKNOWN_ERROR, message=str(e))
    return wrapper