from imgur.models.base import Model
from imgur.enums import AlbumPrivacy, AlbumLayout


class Album(Model):
    def init(self):
        self.id = ''
        self.title = ''
        self.description = ''
        self.datetime = 0
        self.cover = ''
        self.cover_width = 0
        self.cover_height = 0
        self.account_url = None
        self.account_id = None
        self.privacy = AlbumPrivacy.PUBLIC
        self.layout = AlbumLayout.VERTICAL
        self.views = 0
        self.link = ''
        self.favorite = False
        self.nsfw = None
        self.section = ''
        self.order = 0
        self.deletehash = ''
        self.images_count = 0
        self.images = []
        self.in_gallery = False

    def images(self):
        data = self.get(f'/3/album/{self.deletehash}/images').json()['data']
        return [Image(self.session, baseurl=self.baseurl, data=d) for d in data]

    def image(self, image_hash):
        data = self.get(f'/3/album/{self.deletehash}/image/{image_hash}').json()['data']
        return Image(self.session, baseurl=self.baseurl, data=data)

    def update(self, ids=None, deletehashes=None, title=None, description=None, privacy=None, cover=None):
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
        data = self.put(f'/3/album/{self.deletehash}', data=payload).json()
        return data['data']

    def delete(self):
        return super().delete(f'/3/album/{self.deletehash}').json()['data']

    def favorite(self):
        return self.post(f'/3/album/{self.deletehash}/favorite').json()['data']

    def add(self, *image_hashes):
        key = 'ids'
        if self.is_authed:
            key = 'deletehashes'
        payload = {key: ','.join(image_hashes)}
        return self.post(f'/3/album/{self.deletehash}/add', data=payload).json()['data']

    def remove(self, *image_hashes):
        payload = {'ids': ','.join(image_hashes)}
        return self.post(f'/3/album/{self.deletehash}/remove_images', data=payload).json()['data']
