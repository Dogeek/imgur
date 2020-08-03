from imgur.models.base import Model


class AdConfig(Model):
    def __init__(self, session, data=None):
        self.safeFlags = []
        self.highRiskFlags = []
        self.unsafeFlags = []
        self.wallUnsafeFlags = []
        self.showsAds = True

        super().__init__(session, data=data)
