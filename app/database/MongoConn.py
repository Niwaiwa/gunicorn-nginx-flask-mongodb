import logging
from pymongo import MongoClient
from config import setting
from utils.Singleton import Singleton


class MongoConn(Singleton):
    log = logging.getLogger('MongoConn')
    connection = None

    def __connect_db(self):
        self.log.info('connect to Mongo DB')
        return MongoClient(setting.mongo_conn_url, tz_aware=False, connect=False)

    def conn(self):
        if self.connection is None:
            self.connection = self.__connect_db()
        return self.connection

    def venus(self):
        return self.conn()['venus']
