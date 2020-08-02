import json
from urllib.parse import urljoin, urlencode
import webbrowser
from http.server import HTTPServer
import ssl
import os
import logging
import sys
from datetime import datetime
import time

import requests

from imgur.http_server import HandlerInterrupt, RequestHandler

from imgur.controllers.image import ImageController
from imgur.controllers.album import AlbumController
from imgur.controllers.comment import CommentController

from imgur.exceptions import ImgurClientError
from imgur.utils import ImgurSession


class Imgur:
    '''
    Imgur client class. It's the entry point to imgur's API
    '''
    def __init__(self, client_id=None, client_secret=None,
                 access_token=None, refresh_token=None,
                 mashape_key=None, config_file=None, expires_at=1):
        '''
        :param client_id: Imgur client id
        :param client_secret: Imgur client secret
        :param access_token: Imgur access token (can be omitted)
        :param refresh_token: Imgur refresh token (can be omitted)
        :param mashape_key: Key to authenticate commercial imgur apps (can be omitted)
        :param config_file: path to a config file containing the other params
        :param expires_at: Timestamp when the access_token expires
        '''
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
        }
        self.config_file = config_file
        if config_file is not None and os.path.exists(config_file) and not any(params.values()):
            with open(config_file) as f:
                data = json.load(f)
                if not client_id:
                    client_id = data.get('client_id')
                if not client_secret:
                    client_secret = data.get('client_secret')
                if not refresh_token:
                    refresh_token = data.get('refresh_token')
                if not access_token:
                    access_token = data.get('access_token')
                if not mashape_key:
                    mashape_key = data.get('mashape_key')
                if not expires_at:
                    expires_at = data.get('expires_at', time.time())
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
        }
        if not all(params.values()):
            missing = [p for p, pv in params.items() if pv is None]
            raise ImgurClientError(f'Missing parameter : {", ".join(missing)}')

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.baseurl = 'https://api.imgur.com'
        '''Imgur base url. For non commercial apps, this is https://api.imgur.com
        , and 'https://imgur-apiv3.p.rapidapi.com otherwise. A commercial app
        should have a mashape key to authenticate itself, and this is how this library
        determines which baseurl to choose.'''

        self.session = ImgurSession(self)
        '''Instance of imgur.utils.ImgurSession, which handles all the requests
        to imgur's API'''
        if mashape_key:
            self.baseurl = 'https://imgur-apiv3.p.rapidapi.com'
            self.session.headers['X-Mashape-Key'] = mashape_key
        self.session.headers['Authorization'] = f'Client-ID {client_id}'

        formatter = logging.Formatter('%(levelname)s @ %(asctime)s: %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger = logging.Logger('imgur')
        '''logger instance which will log everything to sys.stdout'''
        self.logger.addHandler(handler)

        self.image = ImageController(self.session)
        '''image controller, to handle imgur images'''
        self.album = AlbumController(self.session)
        '''album controller to handle imgur albums'''
        self.comment = CommentController(self.session)
        '''comment controller, to handle imgur comments'''

    def save_config(self, path=None):
        '''
        Saves the current imgur config to $path

        :param path: path to save the config to, the config will be serialized
                     into a json file, loadable by this imgur client
        '''
        path = path or self.config_file
        if path is None:
            return
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'access_token': self.access_token,
            'expires_at': self.expires_at,
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def authorize(self):
        '''
        Authorizes the current application for the logged-in user.

        Runs a webserver to capture the access and refresh tokens, and opens
        the browser to the authorization URI.
        '''
        payload = {
            'client_id': self.client_id,
            'response_type': 'token',
            'state': ''
        }
        certfile = os.path.join(os.path.dirname(__file__), 'server.pem')
        host, port = '127.0.0.1', 8080
        server = HTTPServer((host, port), RequestHandler)
        server.socket = ssl.wrap_socket(
            server.socket,
            certfile=certfile,
            server_side=True
        )
        self.logger.info('Opening auth URL in the browser...')
        webbrowser.open(
            'https://api.imgur.com/oauth2/authorize?' + urlencode(payload)
        )
        self.logger.info('Starting webserver on https://%s:%s/', host, port)
        try:
            server.serve_forever()
        except HandlerInterrupt as interrupt:
            self.access_token = interrupt.access_token
            self.refresh_token = interrupt.refresh_token
            self.expires_at = time.time() + interrupt.expires_in
            self.logger.info('Grabbed the access token %s which expires at %s', self.access_token, datetime.fromtimestamp(self.expires_at))
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
            self.logger.info('Shutting down webserver...')
        self.save_config()

    def authenticate(self):
        '''
        Authenticates the app to imgur. Sets the session's Authorization headers to
        the access token if it is still valid. If it is not, creates a new access_token
        from the refresh token.
        '''
        if time.time() < self.expires_at and self.access_token:
            self.session.headers['Authorization'] = f'Bearer {self.access_token}'
            return self.access_token

        if self.refresh_token is None:
            raise ImgurClientError('Refresh token is required to authenticate.')

        payload = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        response = self.session.post('/oauth2/token', data=payload).json()
        config = conf('imgur')
        config.update({'access_token': response['access_token'], 'refresh_token': response['refresh_token']})
        updateconf('imgur', config)
        self.session.headers['Authorization'] = f'Bearer {response["access_token"]}'
        return response['access_token']
