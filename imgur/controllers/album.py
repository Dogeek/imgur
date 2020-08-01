from imgur.controllers.base import Controller
from imgur.models.album import Album
from imgur.models.image import Image
from imgur.enums import AlbumPrivacy
from imgur.exceptions import ImgurClientError


class AlbumController(Controller):
    def album(self, hash):
        data = self.get(f'/3/album/{hash}').json()['data']
        return Album(self.session, baseurl=self.baseurl, data=data)

    def images(self, hash):
        data = self.get(f'/3/album/{hash}/images').json()['data']
        return [Image(self.session, baseurl=self.baseurl, data=d) for d in data]

    def image(self, album_hash, image_hash):
        data = self.get(f'/3/album/{album_hash}/image/{image_hash}').json()['data']
        return Image(self.session, baseurl=self.baseurl, data=data)

    def create(self, ids=None, deletehashes=None, title=None, description=None, privacy=None, cover=None):
        payload = {}
        if ids is not None:
            payload.update(ids=','.join(ids))
        if deletehashes is not None:
            payload.update(deletehashes=','.join(deletehashes))
        if title is not None:
            payload.update(title=title)
        if description is not None:
            payload.update(description=description)
        if privacy is not None:
            payload.update(privacy=privacy)
        if cover is not None:
            payload.update(cover=cover)
        data = self.post('/2/album', data=payload).json()['data']
        return Album(self.session, baseurl=self.baseurl, data=data)

    def update(self, hash, ids=None, deletehashes=None, title=None, description=None, privacy=None, cover=None):
        payload = {}
        if ids and deletehashes:
            raise ImgurClientError('You must set either ids or deletehashes, not both')
        if ids is not None:
            if isinstance(ids, (list, tuple)):
                ids = [ids]
            payload.update(ids=','.join(ids))
        if deletehashes is not None:
            if isinstance(deletehashes, (list, tuple)):
                deletehashes = [deletehashes]
            payload.update(deletehashes=','.join(deletehashes))
        if title is not None:
            payload.update(title=title)
        if description is not None:
            payload.update(description=description)
        if privacy is not None:
            payload.update(privacy=privacy)
        if cover is not None:
            payload.update(cover=cover)
        data = self.put(f'/3/album/{hash}', data=payload).json()
        return data['data']

    def delete(self, hash):
        return super().delete(f'/3/album/{hash}').json()['data']

    def favorite(self, hash):
        return self.post(f'/3/album/{hash}/favorite').json()['data']

    def add(self, album_hash, *image_hashes):
        key = 'ids'
        if self.is_authed:
            key = 'deletehashes'
        payload = {key: ','.join(image_hashes)}
        return self.post(f'/3/album/{album_hash}/add', data=payload).json()['data']

    def remove(self, album_hash, *image_hashes):
        payload = {'ids': ','.join(image_hashes)}
        return self.post(f'/3/album/{album_hash}/remove_images', data=payload).json()['data']
