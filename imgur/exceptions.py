class ImgurBaseException(Exception):
    pass

class ImgurClientError(ImgurBaseException):
    pass

class ImgurRateLimitExceeded(ImgurClientError):
    def __init__(self, message, headers):
        self.message = message
        self.user_limit = headers['X-RateLimit-UserLimit']
        self.user_remaining = headers['X-RateLimit-UserRemaining']
        self.user_reset = headers['X-RateLimit-UserReset']
        self.client_limit = headers['X-RateLimit-ClientLimit']
        self.client_remaining = headers['X-RateLimit-ClientRemaining']

        self.post_rate_limit = headers.get('X-Post-Rate-Limit-Limit')
        self.post_rate_remaining = headers.get('X-Post-Rate-Limit-Remaining')
        self.post_rate_reset = headers.get('X-Post-Rate-Limit-Reset')

    def __str__(self):
        return self.message
