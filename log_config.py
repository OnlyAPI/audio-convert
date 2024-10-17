import logging
import logging.handlers
import os
from datetime import datetime

# 日志目录
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 使用日期格式化日志文件名
# today = datetime.now().strftime('%Y-%m-%d')

# 日志文件路径
# LOG_FILE = os.path.join(LOG_DIR, f'{today}-app.log')

# 创建日志格式
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMATTER)
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器，日志文件每天轮换
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y-%m-%d")}-app.log'),
    when='midnight',   # 每天轮换日志文件
    interval=1,
    backupCount=7,     # 保留最近7天的日志
    encoding='utf-8'
)
file_handler.setFormatter(LOG_FORMATTER)
file_handler.setLevel(logging.INFO)

# 创建并配置日志记录器
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 捕获所有等级的日志
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
