import mimetypes

from imgur.models.base import Model


class Image(Model):
    '''Represents a single Imgur image'''
    def __init__(self, session, data=None):
        self.id = ''
        self.title = ''
        self.description = ''
        self.datetime = 0
        self.type = ''
        self.animated = False
        self.width = 0
        self.height = 0
        self.size = 0
        self.views = 0
        self.bandwidth = 0
        self.deletehash = ''
        self.name = ''
        self.section = ''
        self.link = ''
        self.gifv = ''
        self.mp4 = ''
        self.mp4_size = 0
        self.looping = False
        self.favorite = False
        self.nsfw = None
        self.vote = ''
        self.in_gallery = False
        super().__init__(session, data)

    def delete(self):
        return self.session.delete(f'/3/image/{self.deletehash}').json()['data']

    def update(self, title=None, description=None):
        payload = {}
        if title is None:
            payload.update(title=title)
        if description is None:
            payload.update(description=description)

        return self.session.post(f'/3/image/{self.deletehash}', data=payload).json()['data']

    def favorite(self):
        return self.session.post(f'/3/image/{self.deletehash}/favorite').json()['data']
