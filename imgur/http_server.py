from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class HandlerInterrupt(Exception):
    def __init__(self, server, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v[0])
        server.shutdown()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        raise HandlerInterrupt(self.server, **parse_qs(self.path[2:]))
