DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'itkpi.pp.ua']
STATIC_ROOT = '/home/tickets/static'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'campaigns': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

CALLBACK_PREFIX = 'http://itkpi.pp.ua:8142'
