import random
import string
import hashlib

def generate_random_string(length):
    """
    生成指定长度的随机字符串
    """
    letters = string.ascii_letters + string.digits
    result = ''.join(random.choice(letters) for _ in range(length))
    return result
def calculate_md5(string):
    """
    计算字符串的MD5值
    """
    # 创建一个MD5对象
    md5 = hashlib.md5()

    # 更新哈希对象的内容
    md5.update(string.encode('utf-8'))

    # 获取哈希值
    result = md5.hexdigest()

    return result