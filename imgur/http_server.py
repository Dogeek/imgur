from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class HandlerInterrupt(BaseException):
    '''
    Interrupt for the HTTP Server. Holds the data for the access token, refresh token
    and for the expires_at query parameters imgurs sends to the callback.
    '''
    def __init__(self, server, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v[0])
        server.shutdown()


class RequestHandler(BaseHTTPRequestHandler):
    '''
    Custom request handler based on http.server.BaseHTTPRequestHandler

    raises an HandlerInterrupt when a GET request is served to the server.
    '''
    def do_GET(self):
        raise HandlerInterrupt(self.server, **parse_qs(self.path[2:]))
