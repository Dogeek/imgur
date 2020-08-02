import pathlib
import mimetypes

from imgur.models.base import Model
from imgur.enums import Vote


class Image(Model):
    '''Represents a single Imgur image'''
    def __init__(self, session, data=None):
        self.id = ''
        '''The ID for the image'''
        self.title = ''
        '''The title of the image'''
        self.description = ''
        '''Description of the image'''
        self.datetime = 0
        '''Time uploaded, epoch time'''
        self.type = ''
        '''Image MIME type'''
        self.animated = False
        '''Is the image animated'''
        self.width = 0
        '''Width of the image, in pixels'''
        self.height = 0
        '''Height of the image, in pixels'''
        self.size = 0
        '''Size of the image, in bytes'''
        self.views = 0
        '''The number of image views'''
        self.bandwidth = 0
        '''Bandwidth consumed by the image, in bytes'''
        self.deletehash = ''
        '''(optional) the delete hash, if you're logged in as the image owner'''
        self.name = ''
        '''(optional) the original file name, if you're logged in as the image owner'''
        self.section = ''
        '''If the image has been categorized, this will contain the image's section (funny, cats, adviceanimals etc)'''
        self.link = ''
        '''The direct link to the image'''
        self.gifv = ''
        '''(optional) the gifv link. Only available if the image is animated and the type is image/gif'''
        self.mp4 = ''
        '''(optional) the direct link to the .mp4. Only available if the image is animated and type is image/gif. A zero (0) value is possible if the video has not been generated'''
        self.mp4_size = 0
        '''(optional) The Content-Length of the mp4'''
        self.looping = False
        '''(optional) Whether the image has a looping animation'''
        self.favorite = False
        '''Indicates if the current user favorited the image'''
        self.nsfw = None
        '''Indicates if the image has been marked as NSFW or not. None if the information is not available'''
        self.vote = ''
        '''The current user's vote on the album, None if not signed in, or the album has not been voted, or the image has not been submitted to the gallery'''
        self.in_gallery = False
        '''Whether the image has been submitted to the gallery'''
        super().__init__(session, data)
        self.vote = AlbumVote(self.vote)

    def delete(self):
        '''
        Deletes this image.

        :return: imgur's base data response
        :rtype: dict
        '''
        return self.session.delete(f'/3/image/{self.deletehash}').json()['data']

    def update(self, title=None, description=None):
        '''
        Updates this image's information

        :param title: The new title of the image, defaults to None
        :type title: str, optional
        :param description: The new description of the image, defaults to None
        :type description: str, optional
        :return: imgur's data response
        :rtype: dict
        '''
        payload = {}
        if title is None:
            payload.update(title=title)
        if description is None:
            payload.update(description=description)

        return self.session.post(f'/3/image/{self.deletehash}', data=payload).json()['data']

    def favorite(self):
        '''
        Favorites this image

        :return: imgur's basic data response
        :rtype: dict
        '''
        return self.session.post(f'/3/image/{self.deletehash}/favorite').json()['data']

    def add_to_album(self, album):
        '''
        Adds this image to an album

        :param album: The album to add this image to
        :type album: imgur.models.album.Album, str
        '''
        id = self.deletehash or self.id

        if isinstance(album, Album):
            album.add(id)
        elif isinstance(album, str):
            self.session.client.album.add(album, id)

    def download(self, path, stream=False, chunk_size=8192):
        '''
        Downloads an image to a path

        :param path: The path to save the image at
        :type path: pathlib.Path, str
        :param stream: should the image be downloaded in chunks, defaults to False
        :type stream: bool, optional
        :param chunk_size: The size of chunks to download, only relevant if
                           stream=True, defaults to 8192
        :type chunk_size: int, optional
        '''
        if isinstance(path, str):
            path = pathlib.Path(path).expanduser()

        if path.is_dir():
            path = path.joinpath(self.name or '.'.join(self.id, mimetypes.guess_extension(self.type)))

        with open(path, 'wb') as f:
            if stream:
                with requests.get(self.link, stream=True) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            else:
                with requests.get(self.link) as r:
                    r.raise_for_status()
                    f.write(r.content)
