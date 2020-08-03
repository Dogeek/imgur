try:
    from praw.models import Subreddit
except ImportError:
    # PRAW is not installed
    class Subreddit:
        pass

from imgur.controllers.base import Controller
from imgur.models.album import Album
from imgur.models.image import Image
from imgur.models.gallery import GalleryTag, GalleryTagInfo
from imgur.enums import (
    GallerySection, GallerySort, GalleryWindow,
    SearchFileType, SearchSize,
)


class GalleryController(Controller):
    def __init__(self, session):
        super().__init__(session)
        self._tags = None

    def gallery(self, section=GallerySection.HOT, sort=GallerySort.VIRAL, page=0,
                window=GalleryWindow.DAY, show_viral=True, mature=False,
                album_previews=False):
        section = GallerySection(str(section)).value
        sort = GallerySort(str(sort)).value
        window = GalleryWindow(str(window)).value

        params = {
            'showViral': show_viral,
            'mature': mature,
            'album_previews': album_previews,
        }

        data = self.session.get(
            f'/3/gallery/{section}/{sort}/{window}/{page}',
            params=payload
        ).json()['data']

        return [Gallery(self.session, data=d) for d in data]

    def subreddit_gallery(self, subreddit, sort=GallerySort.TIME, page=0, window=GalleryWindow.WEEK):
        sort = GallerySort(str(sort)).value
        window = GalleryWindow(str(window)).value

        if isinstance(subreddit, Subreddit):
            subreddit = subreddit.name

        data = self.session.get(
            f'/3/gallery/r/{subreddit}/{sort}/{window}/{page}'
        ).json()['data']

        return [Gallery(self.session, data=d) for d in data]

    def subreddit_image(self, subreddit, image_id):
        if isinstance(subreddit, Subreddit):
            subreddit = subreddit.name

        data = self.session.get(
            f'/3/gallery/r/{subreddit}/{image_id}'
        ).json()['data']

        return Image(self.session, data=data)

    def list_default_tags(self, cache_update=False):
        data = self.session.get('/3/tags').json()['data']
        if self._tags is None or cache_update:
            self._tags = [GalleryTag(self.session, data=d) for d in data['tags']]
        return self._tags

    def tag_info(self, tagname):
        data = self.session.get(f'/3/gallery/tag_info/{tagname}').json()['data']
        return GalleryTagInfo(self.session, data=data)

    def tags(self, gallery_hash):
        data = self.session.get(f'/3/gallery/{gallery_hash}/tags').json()['data']
        return [GalleryTag(self.session, data=d) for d in data]


    def update_tags(self, gallery_hash, item_id, *tags):
        payload = {
            'id': item_id,
            'tags': ','.join(str(t) for t in tags)
        }
        self.session.post(f'/3/gallery/tags/{gallery_hash}', data=payload)

    def search(self, query_string, sort=GallerySort.TIME, page=0, window=GalleryWindow.ALL):
        query = {'q': query_string}
        sort = GallerySort(str(sort)).value
        window = GalleryWindow(str(window)).value

        data = self.session.get(
            f'/3/gallery/search/{sort}/{window}/{page}',
            params=query
        ).json()['data']

        return [Gallery(self.session, data=d) for d in data]

    def advanced_search(self, q_all=None, q_any=None, q_exactly=None,
                        q_not=None, q_type=None, q_size_px=None,
                        sort=GallerySort.TIME, page=0, window=GalleryWindow.ALL):
        '''
        Performs an advanced search on imgur

        :param q_all: Search for all of these words (and), defaults to None
        :type q_all: str, optional
        :param q_any: Search for any of these words (or), defaults to None
        :type q_any: str, optional
        :param q_exactly: Search for exactly this word or phrase, defaults to None
        :type q_exactly: str, optional
        :param q_not: Exclude results matching this, defaults to None
        :type q_not: str, optional
        :param q_type: Show results for any file type
        :type q_type: imgur.enums.SearchFileType, str, mimetype, optional
        :param q_size_px: Size ranges
        :type q_size_px: imgur.enums.SearchSize, str, optional
        :param sort: How to sort results, defaults to GallerySort.TIME
        :type sort: imgur.enums.GallerySort, str, optional
        :param page: Page number, defaults to 0
        :type page: int, optional
        :param window: Date range of the request, defaults to GalleryWindow.ALL
        :type window: imgur.enums.GalleryWindow, str, optional
        '''
        params = {}
        sort = GallerySort(str(sort)).value
        window = GalleryWindow(str(window)).value

        if q_all:
            params.update(q_all=q_all)
        if q_any:
            params.update(q_any=q_any)
        if q_exactly:
            params.update(q_exactly=q_exactly)
        if q_not:
            params.update(q_not=q_not)
        if q_type:
            if isinstance(q_type, tuple):
                # Assume mimetypes.guess_type output
                q_type = q_type[0]
            if isinstance(q_type, str) and q_type.startswith('image/'):
                # Assume mimetype
                q_type.split('/')[1]
            q_type = SearchFileType(q_type).value
            params.update(q_type=q_type)
        if q_size_px:
            q_size_px = SearchSize(q_size_px).value
            params.update(q_size_px=q_size_px)

        data = self.session.get(
            f'/3/gallery/search/{sort}/{window}/{page}',
            params=query
        ).json()['data']

        return [Gallery(self.session, data=d) for d in data]
