from imgur.models.base import Model
from imgur.enums import ReportReason


class Comment(Model):
    '''Represents a single comment on an image, gallery or album'''
    def __init__(self, session, data=None):
        self.id = 0
        self.image_id = ''
        self.comment = ''
        self.author = ''
        self.author_id = 0
        self.on_album = False
        self.album_cover = ''
        self.ups = 0
        self.downs = 0
        self.points = 0.0
        self.datetime = 0
        self.parent_id = 0
        self.deleted = False
        self.vote = None
        self.children = []
        super().__init__(session, data)

    def delete(self):
        return self.session.delete(f'/3/comment/{self.id}').json()['data']

    def replies(self):
        data = self.session.get(f'/3/comment/{self.id}/replies').json()['data']
        return [Comment(self.session, data=d) for d in data]

    def reply(self, comment):
        payload = {
            'image_id': self.image_id,
            'comment': comment,
        }

        return self.session.post(f'/3/comment/{self.id}', data=payload).json()['data']

    def vote(self, vote):
        return self.session.post(f'/3/comment/{self.id}/vote/{vote}').json()['data']

    def upvote(self):
        return self.vote(self.id, 'up')

    def downvote(self):
        return self.vote(self.id, 'down')

    def veto(self):
        return self.vote(self.id, 'veto')

    def report(self, reason):
        if isinstance(reason, str):
            reason = ReportReason[reason.upper()]
        if isinstance(reason, ReportReason):
            reason = ReportReason.value
        payload = dict(reason=reason)
        return self.session.post(f'/3/comment/{self.id}/report', data=payload).json()['data']