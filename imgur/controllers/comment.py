from imgur.controllers.base import Controller
from imgur.models.comment import Comment
from imgur.enums import ReportReason, Vote


class CommentController(Controller):
    def comment(self, id):
        '''
        Fetches a specific comment

        :param id: The ID of the comment to fetch
        :type id: int
        :return: The comment
        :rtype: imgur.models.comment.Comment
        '''
        data = self.session.get(f'/3/comment/{id}').json()['data']
        return Comment(self.session, data=data)

    def create(self, image_id, comment, parent=None):
        '''
        Creates a comment

        :param image_id: The image id to comment under
        :type image_id: str
        :param comment: The body of the comment
        :type comment: str
        :param parent: The description of the comment, defaults to None
        :type parent: str, optional
        :return: The created comment
        :rtype: imgur.models.comment.Comment
        '''
        payload = {
            'image_id': image_id,
            'comment': comment,
        }
        if parent is not None:
            payload.update(parent=parent)

        data = self.session.post('/3/comment', data=payload).json()['data']
        return Comment(self.session, data=data)

    def delete(self, id):
        '''
        Deletes a specific comment

        :param id: The id of the comment to delete
        :type id: int
        :return: Imgur's Basic response
        :rtype: dict
        '''
        return self.session.delete(f'/3/comment/{id}').json()['data']

    def replies(self, id):
        '''
        Fetches the replies for a given comment

        :param id: ID of the comment to fetch the replies of
        :type id: int
        :return: A list of Comment instances representing the replies
        :rtype: list[imgur.models.comment.Comment]
        '''
        data = self.session.get(f'/3/comment/{id}/replies').json()['data']
        return [Comment(self.session, data=d) for d in data]

    def reply(self, id, image_id, comment):
        '''
        Replies to a given comment

        :param id: The id of the comment to reply to
        :type id: int
        :param image_id: The image id of the comment
        :type image_id: str
        :param comment: The body of the comment
        :type comment: str
        :return: Imgur's basic response
        :rtype: dict
        '''
        payload = {
            'image_id': image_id,
            'comment': comment,
        }

        return self.session.post(f'/3/comment/{id}', data=payload).json()['data']

    def vote(self, id, vote):
        '''
        Votes on a specific comment

        :param id: The id of the comment to vote for
        :type id: int
        :param vote: The vote to perform, one of 'up', 'down', or 'veto'
        :type vote: imgur.enums.Vote, str
        :return: Imgur's basic response
        :rtype: dict
        '''
        if isinstance(vote, Vote):
            vote = vote.value
        return self.session.post(f'/3/comment/{id}/vote/{vote}').json()['data']

    def upvote(self, id):
        '''
        Upvotes a comment

        :param id: the id of the comment to upvote
        :type id: int
        :return: Imgur's basic response
        :rtype: dict
        '''
        return self.vote(id, Vote.UP)

    def downvote(self, id):
        '''
        Downvotes a comment

        :param id: the id of the comment to downvote
        :type id: int
        :return: Imgur's basic response
        :rtype: dict
        '''
        return self.vote(id, Vote.DOWN)

    def veto(self, id):
        '''
        Vetoes a comment

        :param id: the id of the comment to veto
        :type id: int
        :return: Imgur's basic response
        :rtype: dict
        '''
        return self.vote(id, Vote.VETO)

    def report(self, id, reason):
        '''
        Reports a comment

        :param id: The id of the comment to report
        :type id: int
        :param reason: The reason for reporting the comment
        :type reason: imgur.enums.ReportReason, str
        :return: Imgur's basic response
        :rtype: dict
        '''
        if isinstance(reason, str):
            reason = ReportReason[reason.upper()]
        if isinstance(reason, ReportReason):
            reason = ReportReason.value
        payload = dict(reason=reason)
        return self.session.post(f'/3/comment/{id}/report', data=payload).json()['data']
