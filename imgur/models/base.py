from urllib.parse import urljoin

class Model:
    BASEURL = 'https://api.imgur.com'

    def __init__(self, session, baseurl=None, data=None):
        self.session = session
        if baseurl:
            self.BASEURL = baseurl
        init()
        if isinstance(data, dict):
            self.set(**data)

    def init(self):
        raise NotImplementedError()

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
