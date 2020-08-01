import re

from imgur.enums import UploadType


def detect_type(img_or_vid):
    if re.search(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', img_or_vid):
        return UploadType.BASE64
    if re.search(r'^https?://', img_or_vid):
        return UploadType.URL
    return UploadType.BINARY


def get_version(version):
    if isinstance(version, str):
        return version
    return '.'.join(str(v) for v in version)