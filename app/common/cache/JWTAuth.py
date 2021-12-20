import logging
from database.RedisConn import RedisClient
from utils.JWT import JWT
from config import setting


class JWTAuth:
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.logging.info("AuthDAO __init__")
        self.redis_conn = RedisClient().conn()

    def save_token(self, user_id: str, token: str, expire_sec: int = setting.auth_token_expire_sec):
        self.logging.info("save_token")
        self.redis_conn.set(user_id, token, ex=expire_sec)

    def del_token(self, user_id: str) -> bool:
        """
        :param user_id: str
        :return: bool 有此token 且刪除成功 回 True
        """
        self.logging.info("del_token")
        # 刪除成功 會回 1, 不存在的key name 沒有刪除成功 回 0
        return True if self.redis_conn.delete(user_id) == 1 else False

    def authenticate(self, request_jwt_token: str):
        """
        user_id 在 redis 取 jwt_token, 並認證token 是否一致
        :param request_jwt_token:
        :return:
        """
        self.logging.info('authenticate')
        jwt_info = JWT.get_jwt_info(request_jwt_token)
        if not jwt_info:
            return False

        user_id = jwt_info['user_id']
        redis_jwt_token = self.redis_conn.get(user_id)
        return jwt_info if redis_jwt_token == request_jwt_token else False
