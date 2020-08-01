from urllib.parse import urljoin


class Controller:
    def __init__(self, session, baseurl=None):
        self.session = session
        self.baseurl = baseurl

    @property
    def is_authed(self):
        return 'Bearer' in self.session.headers['Authorization']

    def request(self, method, endpoint, **kwargs):
        return self.session.request(
            method, urljoin(self.BASEURL, endpoint),
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)
