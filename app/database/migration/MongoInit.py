from database.MongoConn import MongoConn
from pymongo import IndexModel, ASCENDING, DESCENDING


class MongoInit:
    collection_info = {
        'users': [
            IndexModel([("email", ASCENDING)], unique=True),
        ]
    }

    def init_db_index(self, is_rebuild_index: bool = False):
        coll_name_list = MongoConn().venus().list_collection_names()
        for coll_name, indexes in self.collection_info.items():
            if coll_name not in coll_name_list:
                MongoConn().venus().create_collection(coll_name)
            if is_rebuild_index:
                MongoConn().venus()[coll_name].drop_indexes()
            MongoConn().venus()[coll_name].create_indexes(indexes)


if __name__ == "__main__":
    MongoInit().init_db_index()
