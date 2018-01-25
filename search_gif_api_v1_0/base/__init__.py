# coding=utf-8
from flask import Flask
from base.config import config,Config
from redis import StrictRedis
from base.tools import RegexConverter
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
import threadpool
# 设置日志的记录等级
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("mylogs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（应用程序实例app使用的）添加日后记录器
logger.addHandler(file_log_handler)

class CreateApp:
    def __init__(self):
        self.app = Flask(__name__)
    def create_app(self,config_name):
        self.app.config.from_object(config[config_name])
        # 为app中的url路由添加正则表达式匹配
        self.app.url_map.converters["regex"] = RegexConverter
        # 为app添加api蓝图应用
        from api_1_0 import api as api_1_0_blueprint
        self.app.register_blueprint(api_1_0_blueprint, url_prefix="/api/v1.0")
        self.app.redis_con = StrictRedis()
        self.app.pool = threadpool.ThreadPool(100)
        return self.app