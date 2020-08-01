from imgur.controllers.base import Controller
from imgur.models.comment import Comment
from imgur.enums import ReportReason


class CommentController(Controller):
    def comment(self, id):
        data = self.get(f'/3/comment/{id}').json()['data']
        return Comment(self.session, baseurl=self.baseurl, data=data)

    def create(self, image_id, comment, parent=None):
        payload = {
            'image_id': image_id,
            'comment': comment,
        }
        if parent is not None:
            payload.update(parent=parent)

        data = self.post('/3/comment', data=payload).json()['data']
        return Comment(self.session, baseurl=self.baseurl, data=data)

    def delete(self, id):
        return super().delete(f'/3/comment/{id}').json()['data']

    def replies(self, id):
        data = self.get(f'/3/comment/{id}/replies').json()['data']
        return [Comment(self.session, baseurl=self.baseurl, data=d) for d in data]

    def reply(self, id, image_id, comment):
        payload = {
            'image_id': image_id,
            'comment': comment,
        }

        return self.post(f'/3/comment/{id}', data=payload).json()['data']

    def vote(self, id, vote):
        return self.post(f'/3/comment/{id}/vote/{vote}').json()['data']

    def upvote(self, id):
        return self.vote(id, 'up')

    def downvote(self, id):
        return self.vote(id, 'down')

    def veto(self, id):
        return self.vote(id, 'veto')

    def report(self, id, reason):
        if isinstance(reason, str):
            reason = ReportReason[reason.upper()]
        if isinstance(reason, ReportReason):
            reason = ReportReason.value
        payload = dict(reason=reason)
        return self.post(f'/3/comment/{id}/report', data=payload).json()['data']
