from helpers import redis


def test_redis():
    key = "tests:helpers:test_redis"
    redis.redis_manager.delete(key)
    get = redis.redis_manager.get(key)
    assert get is None
    redis.redis_manager.set(key, "test")
    get = redis.redis_manager.get(key)
    assert get == "test"
