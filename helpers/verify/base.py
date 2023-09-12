from helpers import redis
from helpers.verify.abstract import Abstract


class Base(Abstract):
    """
    验证器基类
    """

    def get_cache_data(self, key):
        """
        获取缓存数据
        """
        return redis.redis_manager.get(key)

    def set_cache_data(self, key, value):
        """
        设置缓存数据
        """
        return redis.redis_manager.set(key, value)

    def del_cache_data(self, key):
        """
        删除缓存数据
        """
        return redis.redis_manager.delete(key)
