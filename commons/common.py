import logging
from logging.handlers import TimedRotatingFileHandler

from celery.utils.log import get_task_logger
from commons.custom_handlers import DbHandler
from django.conf import settings

logging.basicConfig(level=logging.NOTSET)


def get_logger(name=''):

    return logging.getLogger('library.{}'.format(name))


def init_celery_logger(name="library"):
    LOG_PATH = settings.CELERY_FPATH
    raw_logger = get_task_logger(name)
    dbHandler = DbHandler()
    dbHandler.setLevel(level=logging.INFO)
    raw_logger.addHandler(dbHandler)
    file_format = logging.Formatter(
        fmt='[%(asctime)s][%(pathname)s][%(filename)s][%(funcName)s][LINE:%(lineno)d][%(levelname)s]:%(message)s')
    fileHandler = TimedRotatingFileHandler(LOG_PATH, when='D', interval=1, backupCount=1,
                                           encoding='utf-8')
    fileHandler.setLevel(level=logging.INFO)
    fileHandler.setFormatter(file_format)
    raw_logger.addHandler(fileHandler)
    return raw_logger


celery_logger = init_celery_logger()
