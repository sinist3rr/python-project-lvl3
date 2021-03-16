def generate_logger_config(level: str) -> dict:
    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'std_format': {
                'format': '{asctime} - {name} - {levelname} - {module}:{funcName}- {message}',  # noqa: E501
                'style': '{'
                }
            },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'std_format'
                }
            },
        'loggers': {
            'page_loader.download_lib': {
                'level': level,
                'handlers': ['console']
                # 'propagate': False
                },
            'urllib3': {
                'level': level,
                'handlers': ['console']
            }
            },
        }
    return logger_config
