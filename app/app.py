from flask import Flask, Blueprint, render_template, jsonify
from flask_cors import CORS
from gevent import pywsgi

import config
from app.models.TaskManager import taskManager
from .views import UserView, RecordView, FileView, TestView, FeatureView, MessageView, NoticeView, AppealView, \
    FeedbackView


def flask_app_run():
    # 初始化flask程序
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/app/static")

    # 设置允许跨域访问
    CORS(app, support_credentials=True)
    # 开启调试模式
    app.debug = config.Debug

    # 启动任务监视线程
    taskManager.start()

    # 初始化view model 模块
    test_blue = TestView.TestBlue
    user_blue = UserView.UserBlue
    file_blue = FileView.FileBlue
    record_blue = RecordView.RecordBlue
    featureblue = FeatureView.FeatureBlue
    noticeblue = NoticeView.NoticeBlue
    messageblue = MessageView.MessageBlue
    appealblue = AppealView.AppealBlue
    feedbackblue = FeedbackView.FeedbackBlue
    # api接口前缀
    apiPrefix = '/api'

    # 主页面蓝图
    main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path="/static")

    main = Blueprint('main', __name__)

    @main.route('/', defaults={'path': ''})
    @main.route('/<path:path>')
    def index(path):
        return render_template('index.html')

    app.register_blueprint(main)
    app.register_blueprint(test_blue)
    app.register_blueprint(user_blue, url_prefix=apiPrefix)
    app.register_blueprint(file_blue, url_prefix=apiPrefix)
    app.register_blueprint(record_blue, url_prefix=apiPrefix)
    app.register_blueprint(featureblue, url_prefix=apiPrefix)

    app.register_blueprint(noticeblue, url_prefix=apiPrefix)
    app.register_blueprint(messageblue, url_prefix=apiPrefix)
    app.register_blueprint(appealblue, url_prefix=apiPrefix)
    app.register_blueprint(feedbackblue, url_prefix=apiPrefix)

    @app.errorhandler(404)
    def page_not_fount(error):
        resData = dict(flag="error", msg="404不存在")
        return jsonify(resData)

    @app.errorhandler(500)
    def page_error_500(error):
        resData = dict(flag="error", msg="500服务器内部错误")
        return jsonify(resData)

    # 原因是DEBUG模式下flask开多一个线程来监视项目的变化。
    # 所以如果是多线程的任务要初始化，在debug模式下初始化一次就会会出现两个实例
    # 如果你想要避免加载两次，应该设置app.run(debug=True, use_reloader=False)
    # app.run(host='127.0.0.1', port=5000, threaded=True, use_reloader=False)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)

    server.serve_forever()
