class ImgurBaseException(Exception):
    pass

class ImgurClientError(ImgurBaseException):
    pass

class ImgurRateLimitExceeded(ImgurClientError):
    pass
