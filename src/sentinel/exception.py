class BaseSentinelError(Exception):
    ...


class NoScenesEnough(BaseSentinelError):
    ...


class ImageModeNotExist(BaseSentinelError):
    ...
