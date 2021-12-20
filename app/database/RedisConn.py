import logging
import redis
from config import setting
from utils.Singleton import Singleton


class RedisClient(Singleton):
    log = logging.getLogger('RedisClient')
    connection = None

    def __connect_redis(self, db: int = 1):
        self.log.info('connect to redis...')

        return redis.Redis(
            host=setting.redis_host,
            port=setting.redis_port,
            password=setting.redis_password,
            ssl=setting.red_is_ssl,
            decode_responses=True,
            db=db
        )

    def conn(self):
        if self.connection is None:
            self.connection = self.__connect_redis()
        return self.connection
