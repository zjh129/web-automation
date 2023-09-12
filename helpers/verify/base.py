from content_tools import settings
from content_tools.libary.verify.abstract import Abstract


class Base(Abstract):
    """
    验证器基类
    """

    def get_cache_data(self, key):
        """
        获取缓存数据
        """
        return settings.RedisCluster.get(key)

    def set_cache_data(self, key, value):
        """
        设置缓存数据
        """
        return settings.RedisCluster.set(key, value)

    def del_cache_data(self, key):
        """
        删除缓存数据
        """
        return settings.RedisCluster.delete(key)
