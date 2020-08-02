import enum


class Vote(enum.Enum):
    '''Options for voting'''
    UP = 'up'
    DOWN = 'down'
    NOT_VOTED = 'none'
    VETO = 'veto'


class UploadType(enum.Enum):
    '''Types of upload accepted by imgur'''
    BASE64 = 'base64'
    URL = 'url'
    BINARY = 'binary'


class AlbumPrivacy(enum.Enum):
    '''Album privacy settings'''
    PUBLIC = 'public'
    HIDDEN = 'hidden'
    SECRET = 'secret'


class AlbumLayout(enum.Enum):
    '''Available album layouts'''
    BLOG = 'blog'
    GRID = 'grid'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class ReportReason(enum.Enum):
    '''Available reasons to report a post'''
    DOESNT_BELONG = 1
    SPAM = 2
    ABUSIVE = 3
    MATURE_UNMARKED = 4
    PORNOGRAPHY = 5
