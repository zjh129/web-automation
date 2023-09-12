from redis import cluster

from configs import redis


class RedisManager:
    def __init__(self, redis_config: dict):
        """
        :param redis_config: redis config
        """
        if redis_config["type"] == "cluster":
            cluster_nodes = []
            for node in redis_config["cluster_nodes"]:
                cluster_nodes.append(cluster.ClusterNode(node["host"], node["port"]))
            self.redis_obj = cluster.RedisCluster(startup_nodes=redis_config, password=redis_config['passwd'],
                                                  decode_responses=True)
        elif redis_config["type"] == "node":
            self.redis_obj = cluster.Redis(host=redis_config["host"], port=redis_config["port"],
                                           password=redis_config['passwd'], decode_responses=True)

    def get_redis(self):
        return self.redis_obj
