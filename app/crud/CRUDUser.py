from database.MongoConn import MongoConn
from bson.objectid import ObjectId
from passlib.context import CryptContext
from typing import Optional

# need pip install bcrypt package, maybe need pip >= 20
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser:

    def __init__(self) -> None:
        self.users_coll = MongoConn().venus()['users']

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(plain_password, hashed_password)
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def get_user_info_by_user_id(self, user_id: str, return_password: bool = False) -> Optional[dict]:
        projection = {} if return_password else {"password": 0}
        return self.users_coll.find_one({'_id': ObjectId(user_id)}, projection)

    def get_user_info_by_email(self, email: str, return_password: bool = False) -> Optional[dict]:
        projection = {} if return_password else {"password": 0}
        return self.users_coll.find_one({'email': email}, projection)

    def check_user_exist(self, email: str) -> bool:
        count = self.users_coll.count_documents({'email': email})
        return True if count > 0 else False

    def create_user(self, email: str, hashed_password: str) -> str:
        result = self.users_coll.insert_one({'email': email, 'password': hashed_password})
        return str(result.inserted_id)

    def delete_user(self, user_id: str) -> Optional[dict]:
        result = self.users_coll.find_one_and_delete({'_id': ObjectId(user_id)})
        return result
