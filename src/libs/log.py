import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

class Log:
    def __init__(self):
        '''制作记录器'''
        log_dirname = 'logs'
        if not os.path.isdir(log_dirname):
            os.makedirs(log_dirname)
        # 处理器
        current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        formatter = logging.Formatter('%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)s | %(message)s')
        # self.fileHandler = logging.FileHandler(filename='{}/{}.review.log'.format(log_dirname, current_time))
        self.fileHandler = TimedRotatingFileHandler(
            filename='{}/{}.txt'.format(log_dirname, current_time), when='H', interval=2, backupCount=36)
        self.fileHandler.setLevel(logging.INFO)
        self.fileHandler.setFormatter(formatter)
        # 过滤器
        filter = logging.Filter('lts')
        # 记录器
        self.logger = logging.getLogger('lts.log')
        # 设置记录器级别
        self.logger.setLevel(logging.INFO)
        # 给记录器添加处理器
        self.logger.addHandler(self.fileHandler)
        # 给记录器添加过滤器
        self.logger.addFilter(filter)
        '''记录器制作完毕'''