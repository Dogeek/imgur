import re
from urllib.parse import urljoin
from http import HTTPStatus
import warnings
import time

from requests import Session

from imgur.enums import UploadType
from imgur.exceptions import ImgurRateLimitExceeded, ImgurNotAuthenticated


def detect_type(img_or_vid):
    '''
    Detects whether an URI is a base64 encoded string, an URL or a binary file.

    :param img_or_vid: The image or video to detect the UploadType of
    :returns: UploadType.BASE54, UploadType.URL or UploadType.BINARY
    :rtype: imgur.enums.UploadType
    '''
    if re.search(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', img_or_vid):
        return UploadType.BASE64
    if re.search(r'^https?://', img_or_vid):
        return UploadType.URL
    return UploadType.BINARY


def get_version(version):
    '''
    Parses a version tuple into a version string

    :param version: version tuple or string
    :type version: Union(tuple, str)
    :returns: version string
    :rtype: str
    '''
    if isinstance(version, str):
        return version
    return '.'.join(str(v) for v in version)

class ImgurSession(Session):
    '''
    A session to make requests to imgur. Inherits from requests.Session.
    '''
    def __init__(self, client, *args, **kwargs):
        '''
        :params baseurl: the base url to use for API calls. It should be
                         'https://api.imgur.com/' unless the app is commercial.
        '''
        super().__init__(*args, **kwargs)
        self.baseurl = client.baseurl
        self.client = client

        self.last_response_headers = {}
        self.etags = {}
        self.response_cache = {}

    def request(self, method, endpoint, **kwargs):
        '''
        Performs a request to imgur. Handles the ETag specification, rate limits
        and deprecations from imgur.

        :param method: The method of the request (GET, POST, PUT, DELETE)
        :type method: str
        :param endpoint: The endpoint to request, will be joined to the base url.
        :type endpoint: str

        :returns: response from the server
        :rtype: requests.Response
        '''
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        etag = self.etags.get(endpoint)
        if etag:
            kwargs['headers'].update({'If-None-Match': etag})

        if not self.rate_limit_reached:
            response = super().request(
                method, urljoin(self.baseurl, endpoint),
                **kwargs
            )
        else:
            raise ImgurRateLimitExceeded('Rate limit reached', self.last_response_headers)

        if 'ETag' in response.headers:
            self.etags[endpoint] = response.headers['ETag']

        self.last_response_headers = response.headers
        if response.status_code == HTTPStatus.NOT_MODIFIED.value:
            response = self.response_cache[endpoint]
        elif method == 'GET':
            self.response_cache[endpoint] = response
        if 'Sunset' in response.headers:
            warnings.warn(f"The endpoint {endpoint} is deprecated. It will be removed on {response.headers['Sunset']}.")
        return response

    @property
    def rate_limit_reached(self):
        '''
        Property that checks the last response headers for rate limting info,
        and returns whether or not the rate limit has been reached
        '''
        reached_user = self.last_response_headers['X-RateLimit-UserRemaining'] <= 0
        reached_app = self.last_response_headers['X-RateLimit-ClientRemaining'] <= 0
        has_reset = self.last_response_headers['X-RateLimit-UserReset'] >= time.time()
        reached_request = (reached_user or reached_app) and not has_reset
        reached_post = self.last_response_headers.get('X-Post-Rate-Limit-Remaining', 1) <= 0
        has_reset_post = self.last_response_headers.get('X-Post-Rate-Limit-Reset', 0) <= 0
        return reached_request and (reached_post and not has_reset_post)

    @property
    def is_authed(self):
        '''
        Property that checks the Authorization request header.

        Imgur supports 2 authorization methods
            - Client-Id : unauthenticated, only using the app's client id
            - Bearer : a bearer OAuth2 token, authenticating the app to the user.

        On the second case, this property returns True, and False otherwise
        '''
        return 'Bearer' in self.session.headers['Authorization']


def auth_required(func):
    '''
    A decorator for methods that only support calls
    from authenticated apps.
    '''
    def decorated(self, *args, **kwargs):
        if self.session.is_authed:
            return func(self, *args, **kwargs)
        raise ImgurNotAuthenticated(f'You must be authenticated to call {func.__name__}')
    return decorated
