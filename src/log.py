import os
from datetime import datetime

from pythonjsonlogger import jsonlogger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CustomJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict, **kwargs):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        if log_record.get('color_message'):
            del log_record['color_message']

        if log_record.get('message'):
            log_record['message'] = log_record.get('message').replace('"', '\'')
        
        if log_record.get('exc_info'):
            log_record['exc_info'] = log_record.get('exc_info').replace('"', '\'')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json_default': {
            '()': 'log.CustomJsonFormatter',
            'format': '%(timestamp)s %(level)s %(message)s',
        },
        'json_default_access': {
            '()': 'log.CustomJsonFormatter',
            'format': '%(levelprefix)s %(message)s',
        },
        'json_access': {
            '()': 'log.CustomJsonFormatter',
            'format': '%(timestamp)s %(level)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/app.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'file_server': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'file_db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/db.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'json_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json_default',
            'filename': os.path.join(BASE_DIR, 'logs/app.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'json_file_server': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json_default',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'json_file_server_access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json_access',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'json_file_server_default_access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json_default_access',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
        'json_file_db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json_default',
            'filename': os.path.join(BASE_DIR, 'logs/db.log'),
            'maxBytes': (1024 * 1024) * 50,
            'backupCount': 25,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['json_file_server'],
            'level': 'INFO'
        },
        'uvicorn.error': {
            'handlers': ['json_file_server_default_access', 'default',],
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['json_file_server_access', 'access',],
            'level': 'INFO',
            'propagate': False
        },
        'app': {
            'handlers': ['json_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'db': {
            'handlers': ['json_file_db'],
            'level': 'INFO',
            'propagate': False,
        },
        # 'sqlalchemy.engine': {
        #     'handlers': ['console', 'file_db'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # }
    }
}