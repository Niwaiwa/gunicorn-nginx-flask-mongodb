import logging
import traceback
from common.cache.JWTAuth import JWTAuth
from common.Response import response
from crud.CRUDUser import CRUDUser
from flask import request, g
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from redis.exceptions import RedisError
from schemas.User import User, UserLogin
from utils.JWT import JWT


class AuthAPI:
    logging = logging.getLogger(__name__)

    def register(self):
        AuthAPI.logging.info('register')
        try:
            data = request.get_json(silent=True)
            if data is None:
                return response(2, http_code=401)

            user_data = User(**data)

            crud_user = CRUDUser()
            if crud_user.check_user_exist(user_data.email):
                AuthAPI.logging.info('user existed')
                return response(3, http_code=401)

            password_hashed = crud_user.get_password_hash(user_data.password)
            user_id = crud_user.create_user(user_data.email, password_hashed)

            token = JWT().gen_jwt_token(user_id)
            JWTAuth().save_token(user_id, token)

            headers = {'Authorization': token}
            return response(0, data={'email': user_data.email}, http_code=201, headers=headers)
        except ValidationError as e:
            AuthAPI.logging.info(e.json(indent=None))
            return response(2, http_code=401)
        except RedisError as e:
            AuthAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(4, http_code=503)
        except PyMongoError as e:
            AuthAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(2, http_code=503)

    def login(self):
        AuthAPI.logging.info('login')
        try:
            data = request.get_json(silent=True)
            if data is None:
                return response(5, http_code=401)

            user_data = UserLogin(**data)

            crud_user = CRUDUser()
            user_info = crud_user.get_user_info_by_email(user_data.email, True)
            if not user_info:
                return response(5, http_code=401)

            if crud_user.verify_password(user_data.password, user_info['password']) is False:
                AuthAPI.logging.info('user password invalid')
                return response(5, http_code=401)

            user_id = str(user_info['_id'])
            token = JWT().gen_jwt_token(user_id)
            JWTAuth().del_token(user_id)
            JWTAuth().save_token(user_id, token)

            headers = {'Authorization': token}
            return response(0, data={'email': user_data.email}, http_code=200, headers=headers)
        except ValidationError as e:
            AuthAPI.logging.info(e.json(indent=None))
            return response(5, http_code=401)
        except RedisError as e:
            AuthAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(6, http_code=503)
        except PyMongoError as e:
            AuthAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(6, http_code=503)

    def logout(self):
        AuthAPI.logging.info('logout')
        try:
            JWTAuth().del_token(g.user_id)
            return response(0, http_code=204)
        except RedisError as e:
            AuthAPI.logging.info(traceback.format_exc().replace("\n", ""))
            return response(6, http_code=503)
