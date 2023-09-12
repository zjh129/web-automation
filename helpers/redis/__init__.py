from configs.redis import REDIS
from helpers.redis.redis_manager import RedisManager

# 定义redis管理器
redis_manager = RedisManager(redis_config=REDIS)