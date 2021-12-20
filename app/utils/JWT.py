import jwt
import time
import logging
from config import setting


class JWT:
    logging = logging.getLogger(__name__)

    @staticmethod
    def gen_jwt_token(user_id: str) -> str:
        """
        產生jwt token, 將 user_id 放入token資訊內
        :param user_id:
        :return:
        """
        return jwt.encode({'user_id': user_id, 'timestamp': time.time()}, setting.secret_key, algorithm='HS256')

    @staticmethod
    def get_jwt_info(jwt_token: str):
        """
        從jwt token decrypt 取得jwt_info
        :param jwt_token:
        :return:
        """
        try:
            jwt_info = jwt.decode(jwt_token, key=setting.secret_key, algorithms=['HS256'])
            return jwt_info
        except jwt.exceptions.InvalidSignatureError as e:
            JWT.logging.debug(e.__str__())
            return False
        except jwt.InvalidTokenError as e:
            JWT.logging.debug(e.__str__())
            return False
