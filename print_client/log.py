import logging
import os




def get_logger():
    # 配置日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 创建日志格式化器
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d -  %(levelname)s- %(message)s')

    # 创建文件处理器
    file_handler = logging.FileHandler('./log.txt',encoding="utf8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器中
    logger.addHandler(file_handler)
    return logger
