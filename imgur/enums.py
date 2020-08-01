import enum


class UploadType(enum.Enum):
    BASE64 = 'base64'
    URL = 'url'
    BINARY = 'binary'


class AlbumPrivacy(enum.Enum):
    PUBLIC = 'public'
    HIDDEN = 'hidden'
    SECRET = 'secret'


class AlbumLayout(enum.Enum):
    BLOG = 'blog'
    GRID = 'grid'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class ReportReason(enum.Enum):
    DOESNT_BELONG = 1
    SPAM = 2
    ABUSIVE = 3
    MATURE_UNMARKED = 4
    PORNOGRAPHY = 5
