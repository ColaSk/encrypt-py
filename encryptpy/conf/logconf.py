
def logconfig(log_file):

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'simple',
                'filename': log_file,
                'backupCount': 10,
                'encoding': 'utf-8'
            }
        },
        'root': {
            'handlers': ['console', 'default'],
            'level': 'INFO'
        }
    }