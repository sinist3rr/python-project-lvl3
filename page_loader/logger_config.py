import logging


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno <= logging.INFO


def generate_logger_config(level: int) -> dict:
    logger_config = {
        'version': 1,
        'filters': {
            'stdout_filter': {
                '()': InfoFilter,
            }
        },
        'disable_existing_loggers': False,

        'formatters': {
            'std_format': {
                'format': '{asctime} - {name} - {levelname} - {module}:{funcName}- {message}',  # noqa: E501
                'style': '{'
                }
            },
        'handlers': {
            'console_out': {
                'class': 'logging.StreamHandler',
                'filters': ['stdout_filter'],
                'stream': 'ext://sys.stdout',
                'level': 'DEBUG',
                'formatter': 'std_format'
                },
            'console_err': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
                'level': 'ERROR',
                'formatter': 'std_format'
            }
            },
        'loggers': {
            'page_loader.download_lib': {
                'level': level,
                'handlers': ['console_out', 'console_err']
                # 'propagate': False
                },
            'urllib3': {
                'level': level,
                'handlers': ['console_out', 'console_err']
            }
            },
        }
    return logger_config
