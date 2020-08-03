import enum


__all__ = (
    'Vote', 'UploadType', 'AlbumPrivacy',
    'AlbumLayout', 'ReportReason',
    'FavoriteSort', 'GallerySection',
    'GallerySort', 'GalleryWindow',
    'SearchFileType', 'SearchSize',
)

class _Enum(enum.Enum):
    def __str__(self):
        return str(self.value)


class Vote(_Enum):
    '''Options for voting'''
    UP = 'up'
    DOWN = 'down'
    NOT_VOTED = 'none'
    VETO = 'veto'


class UploadType(_Enum):
    '''Types of upload accepted by imgur'''
    BASE64 = 'base64'
    URL = 'url'
    BINARY = 'binary'


class AlbumPrivacy(_Enum):
    '''Album privacy settings'''
    PUBLIC = 'public'
    HIDDEN = 'hidden'
    SECRET = 'secret'


class AlbumLayout(_Enum):
    '''Available album layouts'''
    BLOG = 'blog'
    GRID = 'grid'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class ReportReason(_Enum):
    '''Available reasons to report a post'''
    DOESNT_BELONG = 1
    SPAM = 2
    ABUSIVE = 3
    MATURE_UNMARKED = 4
    PORNOGRAPHY = 5


class FavoriteSort(_Enum):
    '''Available sorts for gallery favorites'''
    NEWEST = 'newest'
    OLDEST = 'oldest'


class GallerySort(_Enum):
    '''Available sorts for galleries'''
    VIRAL = 'viral'
    TOP = 'top'
    TIME = 'time'
    RISING = 'rising'


class GallerySection(_Enum):
    '''Available sections for galleries'''
    HOT = 'hot'
    TOP = 'top'
    USER = 'user'


class GalleryWindow(_Enum):
    '''Date range of the request if the section is GallerySection.TOP'''
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'
    ALL = 'all'


class SearchFileType(_Enum):
    JPG = 'jpg'
    PNG = 'png'
    GIF = 'gif'
    ANIGIF = 'anigif'
    ALBUM = 'album'


class SearchSize(_Enum):
    SMALL = 'small'
    MEDIUM = 'med'
    MED = 'med'
    BIG = 'big'
    LARGE = 'lrg'
    LRG = 'lrg'
    HUGE = 'huge'