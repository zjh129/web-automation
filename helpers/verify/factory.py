from content_tools.libary.verify.abstract import Abstract
from content_tools.libary.verify.verify_ddddocr import DdddOcrVerify

VERIFY_TYPE_YDM = "ydm"  # 云码，官网：https://www.jfbym.com/
VERIFY_TYPE_CJY = "CJY"  # 超级鹰,官网：https://www.chaojiying.com/
VERIFY_TYPE_DDDDOCR = "ddddocr"  # 带带弟弟，官网：https://github.com/sml2h3/ddddocr


def create_verify(type: str) -> Abstract:
    """
    验证码工厂方法
    """
    if type == VERIFY_TYPE_YDM:
        # 云码类型
        from content_tools.libary.verify.verify_ydm import VerifyYdm
        # token可从配置中获取，目前写死
        return VerifyYdm(token="288PYUoIsPS4xxC7S0yqeLvDiZ5toYd61bjNXO9dTfk")
    elif type == VERIFY_TYPE_DDDDOCR:
        return DdddOcrVerify()
    else:
        raise Exception(f"验证码类型错误：{type}")
