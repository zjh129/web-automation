import json

import redis
from redis import cluster


class RedisManager:
    def __init__(self, redis_config: dict):
        """
        :param redis_config: redis config
        """
        if redis_config["type"] == "cluster":
            cluster_nodes = []
            for node in redis_config["cluster_nodes"]:
                cluster_nodes.append(cluster.ClusterNode(node["host"], node["port"]))
            self.redis_obj = cluster.RedisCluster(startup_nodes=cluster_nodes, password=redis_config['passwd'],
                                                  decode_responses=True)
        elif redis_config["type"] == "node":
            self.redis_obj = redis.Redis(host=redis_config["host"], port=redis_config["port"],
                                         password=redis_config['passwd'], db=0, protocol=3, decode_responses=True)
        # 健康检查
        self.redis_obj.ping()

    def get_redis(self):
        return self.redis_obj

    def set(self, key, value, ex=None, px=None, nx=False, xx=False, is_json=True):
        """
        设置值
        :param key: 键
        :param value: 值 可以是str，也可以是dict 如果是dict，需要设置json=True 使用json存储
        :param is_json: 是否使用json
        :param ex: 过期时间，单位秒
        :param px: 过期时间，单位毫秒
        :param nx: 如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)效果一样
        :param xx: 如果设置为True，则只有name存在时，当前set操作才执行
        :return:
        """
        if is_json:
            try:
                value = json.dumps(value)
            except TypeError:
                pass
        return self.redis_obj.set(key, value, ex, px, nx, xx)

    def get(self, key, is_json=True):
        """
        获取值
        :param key: 键
        :param is_json: 是否使用json
        :return:
        """
        value = self.redis_obj.get(key)
        # 如果是json格式，则转换为dict
        if is_json and value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    def delete(self, key):
        """
        删除
        :param key:
        :return:
        """
        return self.redis_obj.delete(key)
