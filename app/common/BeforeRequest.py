import logging
from flask import request, g
from common.Response import response
from common.cache.JWTAuth import JWTAuth
from config import setting
from crud.CRUDUser import CRUDUser


class BeforeRequest:
    def __init__(self):
        """
        Before all request handle
        """
        self.logging = logging.getLogger(__name__)
        self.logging.info('before_request')

        environ = request.headers.environ
        self.logging.info('Header')
        self.logging.debug(environ)
        self.request_path = environ['PATH_INFO']

    def handle(self):
        """
        Before all request handle
        若有其他需要處理的 加在此部分即可
        :return:
        """
        self.logging.info("handle")

        if self.request_path in setting.verify_exception_paths:
            return

        return self._user_auth()

    def _user_auth(self):
        """
        JWT Token 認證
        :return:
        """
        self.logging.info("_user_auth")

        jwt_token = request.headers.get('Authorization', None)

        self.logging.info(f'jwt_token: {jwt_token}')

        try:
            auth = JWTAuth().authenticate(jwt_token)  # 驗證 user_id 以及 token
        except Exception as e:
            logging.error(e)
            # Token 認證失敗 回傳http code 401
            return response(7, http_code=401)

        if auth:
            user_id = auth['user_id']
            user_info = CRUDUser().get_user_info_by_user_id(user_id)

            # user 資訊存入 global variable
            g.user_info = user_info
            g.user_id = user_id
            g.jwt_token = jwt_token
            return
        else:
            # Token 認證失敗 回傳http code 401
            return response(7, http_code=401)
