class AppInternalError(Exception):
    pass


class FileError(AppInternalError):
    pass


class NetworkError(AppInternalError):
    pass
