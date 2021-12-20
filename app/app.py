import logging
import os
import traceback
from flask import Flask, abort, jsonify, send_from_directory
from config import setting
from config.logging import RequestFormatter
from common.Response import response
from common.BeforeRequest import BeforeRequest
from api.AuthAPI import AuthAPI
from api.UserAPI import UserAPI
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

formatter = RequestFormatter(
    '[%(uuid)s] - %(asctime)s - (%(process)d-%(thread)d) - %(name)s[%(levelname)s] - %(message)s'
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.add_url_rule('/login', view_func=AuthAPI().login, methods=('POST',))
app.add_url_rule('/logout', view_func=AuthAPI().logout, methods=('POST',))
app.add_url_rule('/register', view_func=AuthAPI().register, methods=('POST',))
app.add_url_rule('/user', view_func=UserAPI().delete_user, methods=('DELETE',))

@app.route("/")
def hello_world():
    import pytz
    from datetime import datetime
    TZ = pytz.timezone('Asia/Taipei')
    return f"<p>Server running {setting.env_mode} time: {datetime.now(TZ)} version: v{setting.version}</p>"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.before_request
def before_request():
    return BeforeRequest().handle()

# @app.teardown_request
# def teardown_request(exception=None):
#     if exception:
#         logging.error(exception)
#     request_path = request.headers.environ['PATH_INFO']
#     if request_path in setting.VerifyExceptionPaths[:3]:
#         return
#     TeardownRequest().audit_log()

@app.errorhandler(Exception)
def catch_exception(e):
    # if isinstance(e, HTTPException):
    #     return e
    logger.error(traceback.format_exc().replace("\n", ""))
    return response(1, 'server error', http_code=500)


if __name__ == "__main__":
    # from database.migration.MongoInit import MongoInit
    # MongoInit().init_db_index()
    app.run('0.0.0.0', 8000)
