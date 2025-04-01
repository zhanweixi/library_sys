import logging
import datetime


class DbHandler(logging.Handler):
    '''自定义DB日志handler'''

    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)

    def emit(self, record):
        try:
            from apps.basic.models import LogMsg
            try:
                log_created_at = record.asctime
            except:
                try:
                    log_created_at = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
                except:
                    log_created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            document = {
                'asctime': log_created_at,
                'pathname': record.pathname,
                'filename': record.filename,
                'funcName': record.funcName,
                'line_no': record.lineno,
                'levelname': record.levelname,
                'message': record.getMessage(),
                'remark': record.exc_text
            }
            LogMsg.objects.create(**document)
            return True
        except Exception as e:
            print('write log to db error and error msg is %s' % str(e))
            return False
