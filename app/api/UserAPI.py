import logging
import traceback
from common.Response import response
from common.cache.JWTAuth import JWTAuth
from crud.CRUDUser import CRUDUser
from flask import g
from pymongo.errors import PyMongoError


class UserAPI:
    logging = logging.getLogger(__name__)

    def delete_user(self):
        try:
            JWTAuth().del_token(g.user_id)
            _ = CRUDUser().delete_user(g.user_id)
            return response(0, http_code=204)
        except PyMongoError as e:
            UserAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(1, http_code=503)
