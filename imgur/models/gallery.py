from imgur.models.base import Model
from imgur.models.ads import AdConfig


class GalleryTagInfo(Model):
    def __init__(self, session, data=None):
        self.name = ''
        self.display_name = ''
        self.followers = 0
        self.total_items = 0
        self.following = False
        self.background_hash = ''
        self.is_promoted = False
        self.description = ''
        self.logo_hash = None
        self.logo_destination_url = None
        self.description_annotations = {}

        super().__init__(session, data=data)

class GalleryTag(Model):
    def __init__(self, session, data=None):
        self.id = ''
        self.name = ''
        self.display_name = ''
        self.followers = 0
        self.total_items = 0
        self.background_hash = ''

        super().__init__(session, data=data)

    def __str__(self):
        return self.name

    def info(self):
        data = self.session.get(f'/3/gallery/tag_info/{self.name}').json()['data']
        return GalleryTagInfo(self.session, data=data)


class Gallery(Model):
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
        self.vote = NoneType()
        self.favorite = False
        self.nsfw = False
        self.section = ''
        self.account_url = ''
        self.account_id = 0
        self.is_ad = False
        self.in_most_viral = False
        self.has_sound = False
        self.tags = []
        self.ad_type = 0
        self.ad_url = ''
        self.edited = 0
        self.in_gallery = False
        self.topic = ''
        self.topic_id = 0
        self.link = ''
        self.ad_config = {}
        self.comment_count = 0
        self.favorite_count = 0
        self.ups = 0
        self.downs = 0
        self.points = 0
        self.score = 0
        self.is_album = False

        super().__init__(session, data=data)
        if self.ad_config:
            self.ad_config = AdConfig(self.session, data=self.ad_config)