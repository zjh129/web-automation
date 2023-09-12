import re

from django.http import JsonResponse


def api_json_response(code=0, message='success', data=None):
    """
    返回json格式的数据
    :param code: 错误码
    :param message: 错误信息
    :param data: 数据
    """
    return JsonResponse({'code': code, 'message': message, 'data': data})


def mq_json_response(code=0, message='success', data=None):
    """
    返回json格式的数据
    :param code: 错误码
    :param message: 错误信息
    :param data: 数据
    """
    return {'code': code, 'message': message, 'data': data}


def validate_phone_number(phone_number):
    """
    验证手机号码是否合法（正则表达式匹配中国的手机号码，手机号码为以1开头的11位数字）
    :param phone_number: 手机号码
    :return: 是否合法
    """
    pattern = re.compile("^1[3-9]\d{9}$")
    return bool(pattern.match(phone_number))
