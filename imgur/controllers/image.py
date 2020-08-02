from imgur.models.image import Image
from imgur.utils import detect_type
from imgur.exceptions import ImgurUploadError
from imgur.controllers.base import Controller


class ImageController(Controller):
    def image(self, image_hash):
        data = self.session.get(f'/3/image/{image_hash}').json()['data']
        return Image(self.session, data=data)

    def upload(self, image=None, video=None, album=None, type=None,
                     name=None, title=None, description=None,
                     disable_audio=True):
        if (image is None and video is None) or (image is not None and video is not None):
            raise ImgurUploadError('You need to provide either an image or a video to upload')

        accepted_types = (
            'video/mp4', 'video/webm', 'video/x-matroska', 'video/quicktime',
            'video/x-flv', 'video/x-msvideo', 'video/x-ms-wmv', 'video/mpeg',
        )

        if video is not None and mimetypes.guess_type(video)[0] not in accepted_types:
            raise ImgurUploadError('Video mimetype is not accepted. Accepted types: {", ".join(t.split("/")[1] for t in accepted_types)}')

        payload = {}
        if image is not None:
            payload.update(image=image)
        if video is not None:
            payload.update(video=video)
        if album is not None:
            payload.update(album=album)
        if type is None:
            payload.update(type=detect_type(image or video).value)
        else:
            payload.update(type=type)
        if name is None:
            payload.update(name=name)
        if title is None:
            payload.update(title=title)
        if description is None:
            payload.update(description=description)
        if video is not None:
            payload.update(disable_audio=int(disable_audio))

        data = self.post('/3/upload', data=payload).json()['data']
        return Image(self.session, data=data)

    def delete(self, hash):
        return self.session.delete(f'/3/image/{hash}').json()['data']

    def update(self, hash, title=None, description=None):
        payload = {}
        if title is None:
            payload.update(title=title)
        if description is None:
            payload.update(description=description)

        return self.session.post(f'/3/image/{hash}', data=payload).json()['data']

    def favorite(self, hash):
        return self.session.post(f'/3/image/{hash}/favorite').json()['data']
