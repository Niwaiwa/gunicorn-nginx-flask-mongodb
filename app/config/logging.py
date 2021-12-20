import logging
import uuid
import flask
from flask import g


class RequestFormatter(logging.Formatter):
    """
    讓flask 每一請求的所有log 有 一樣uuid, log搜尋時 就可以只搜尋uuid 就列出當次request的所有log
    """
    log_uuid = None

    def format(self, record):
        if flask.has_request_context():  # if flask context is exists then set the g variable
            g.uuid = uuid.uuid4().hex if 'uuid' not in g else g.uuid
            self.log_uuid = None if 'uuid' not in g else g.uuid
        record.uuid = self.log_uuid

        return super().format(record)
