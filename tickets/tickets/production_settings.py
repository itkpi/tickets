import os

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'tickets.itkpi.pp.ua']
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

EMAIL_HOST = os.environ.get('TICKETS_EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('TICKETS_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('TICKETS_EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[TEDX TICKETS] '
EMAIL_USE_TLS = True
