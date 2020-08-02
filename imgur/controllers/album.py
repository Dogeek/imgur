from imgur.controllers.base import Controller
from imgur.models.album import Album
from imgur.models.image import Image
from imgur.enums import AlbumPrivacy
from imgur.exceptions import ImgurClientError


class AlbumController(Controller):
    def album(self, hash):
        '''
        Gets an album's data

        :param hash: album hash of the album to fetch
        :type hash: str
        :returns: The album model for that album hash
        :rtype: imgur.models.album.Album
        '''
        data = self.session.get(f'/3/album/{hash}').json()['data']
        return Album(self.session, data=data)

    def images(self, hash):
        '''
        Get an album's images

        :param hash: album hash of the album to fetch
        :type hash: str
        :returns: A list of all the images in the album
        :rtype: list[imgur.models.image.Image]
        '''
        data = self.session.get(f'/3/album/{hash}/images').json()['data']
        return [Image(self.session, data=d) for d in data]

    def image(self, album_hash, image_hash):
        '''
        Gets a specific image from an album

        :param album_hash: album hash of the album to fetch
        :type hash: str
        :param image_hash: image hash of the image to fetch
        :type hash: str
        :returns: The image from the appropriate album
        :rtype: imgur.models.image.Image
        '''
        data = self.session.get(f'/3/album/{album_hash}/image/{image_hash}').json()['data']
        return Image(self.session, data=data)

    def create(self, ids=None, deletehashes=None, title=None, description=None, privacy=None, cover=None):
        '''
        Creates an imgur album

        :param ids: IDs of images to add to the album
        :type ids: list[str]
        :param deletehashes: Delete hashes of the images to add to the album
        :type deletehashes: list[str]
        :param title: title of the album
        :type title: str
        :param description: description (subtitle) of the album
        :type description: str
        :param privacy: privacy setting for the album, defaults to 'public'
        :type privacy: Union(imgur.enums.AlbumPrivacy, str)
        :param cover: id of the cover image
        :type cover: str
        :returns: the created album
        :rtype: imgur.models.album.Album
        '''
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
            if isinstance(privacy, AlbumPrivacy):
                privacy = AlbumPrivacy.value
            payload.update(privacy=privacy)
        if cover is not None:
            payload.update(cover=cover)
        data = self.session.post('/2/album', data=payload).json()['data']
        return Album(self.session, data=data)

    def update(self, hash, ids=None, deletehashes=None, title=None, description=None, privacy=None, cover=None):
        '''
        Updates an imgur album

        :param hash: Album hash to update
        :type hash: str
        :param ids: IDs of images to set for the album (will overwrite existing images)
        :type ids: list[str]
        :param deletehashes: Delete hashes of images to set for the album (will overwrite existing images)
        :type deletehashes: list[str]
        :param title: title of the album
        :type title: str
        :param description: description (subtitle) of the album
        :type description: str
        :param privacy: privacy setting for the album, defaults to 'public'
        :type privacy: Union(imgur.enums.AlbumPrivacy, str)
        :param cover: id of the cover image
        :type cover: str
        :returns: imgur basic response
        :rtype: dict
        '''
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
            if isinstance(privacy, AlbumPrivacy):
                privacy = AlbumPrivacy.value
            payload.update(privacy=privacy)
        if cover is not None:
            payload.update(cover=cover)
        data = self.session.put(f'/3/album/{hash}', data=payload).json()
        return data['data']

    def delete(self, hash):
        '''
        Deletes an album

        :param hash: hash of the album to delete
        :returns: imgur's basic data response
        :rtype: dict
        '''
        return self.session.delete(f'/3/album/{hash}').json()['data']

    def favorite(self, hash):
        '''
        Favorites an album

        :param hash: hash of the album to favorite
        :returns: imgur's basic data response
        :rtype: dict
        '''
        return self.session.post(f'/3/album/{hash}/favorite').json()['data']

    def add(self, album_hash, *image_hashes):
        '''
        Adds images to an album

        :param album_hash: hash of the album to add images to
        :param *image_hashes: hashes of the images to add to the album
        :returns: imgur's basic data response
        :rtype: dict
        '''
        key = 'ids'
        if self.is_authed:
            key = 'deletehashes'
        payload = {key: ','.join(image_hashes)}
        return self.session.post(f'/3/album/{album_hash}/add', data=payload).json()['data']

    def remove(self, album_hash, *image_hashes):
        '''
        Removes images from an album

        :param album_hash: hash of the album to remove images from
        :param *image_hashes: hashes of the images to remove from the album
        :returns: imgur's basic data response
        :rtype: dict
        '''
        payload = {'ids': ','.join(image_hashes)}
        return self.session.post(f'/3/album/{album_hash}/remove_images', data=payload).json()['data']
