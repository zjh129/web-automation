from helpers import log
from helpers.common import mq_json_response
from libary.exceptions import ActionException


def exception_handler(func):
    """
    异常处理装饰器
    """
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return mq_json_response(message="执行成功", data=data)
        except ActionException as e:
            return mq_json_response(code=e.code, message=e.message)
        except Exception as e:
            log.logger.error(f"执行异常：{str(e)}", exc_info=True)
            return mq_json_response(code=ActionException.CODE_UNKNOWN_ERROR, message=str(e))
    return wrapper