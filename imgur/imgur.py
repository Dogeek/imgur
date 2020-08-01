from imgur.controllers.image import ImageController
from imgur.controllers.album import AlbumController


class Imgur:
    def __init__(self, client_id, client_secret, access_token, refresh_token, mashape_key=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        baseurl = None

        self.session = requests.session()
        if mashape_key:
            baseurl = 'https://imgur-apiv3.p.rapidapi.com/'
            self.session.headers['X-Mashape-Key'] = mashape_key
        self.session.headers['Authorization'] = f'Client-ID {client_id}'
        self.image = ImageController(self.session, baseurl=baseurl)
        self.album = AlbumController(self.session, baseurl=baseurl)

    def authenticate(self):
        payload = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        response = self.post(
            '/oauth2/token',
            data=payload,
        ).json()
        config = conf('imgur')
        config.update({'access_token': response['access_token'], 'refresh_token': response['refresh_token']})
        updateconf('imgur', config)
        self.session.headers['Authorization'] = f'Bearer {response["access_token"]}'
        return response['access_token']
