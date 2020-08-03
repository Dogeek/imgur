from imgur.controllers.base import Controller
from imgur.models.account import Account, MeAccount
from imgur.exceptions import ImgurNotAuthenticated
from imgur.enums import FavoriteSort


class AccountController(Controller):
    '''Controller for account requests'''
    def __init__(self, session):
        super().__init__(session)
        self._me = None

    @property
    def me(self):
        if self._me is None:
            if self.session.client.username is None:
                raise ImgurNotAuthenticated("You must be authenticated to access the authenticated account's data")
            self._me = self.account(self.session.client.username, me=True)
        return self._me

    def account(self, username, me=False):
        '''
        Gets an account's information

        :param username: The username of the account to fetch
        :type username: str
        :param me: Whether the return value should be an Account or MeAccount instance, defaults to False
        :type me: bool, optional
        :return: The account model
        :rtype: imgur.models.account.Account, imgur.models.account.MeAccount
        '''
        klass = Account if not me else MeAccount
        data = self.session.get(f'/3/account/{username}').json()['data']
        return klass(self.session, data=data)

    def blocked(self, username):
        '''
        Whether the username is blocked for the logged in account

        :param username: The username to check for
        :type username: str
        :return: Whether the user is blocked or not
        :rtype: bool
        '''
        data = self.session.get(f'account/v1/{username}/block').json()['data']
        return data['blocked']

    def block(self, username):
        self.session.post(f'/account/v1/{username}/block')

    def unblock(self, username):
        self.session.delete(f'/account/v1/{username}/block')

    def gallery_favorites(self, username, page=None, sort=None):
        if sort is None:
            sort = FavoriteSort.NEWEST
        if isinstance(sort, FavoriteSort):
            sort = sort.value

        query = ''
        if page:
            query += f'/{page}/{sort}'

        data = self.get(f'/3/account/{username}/gallery_favorites{query}').json()['data']
        return data  # TODO: GalleryImage or GalleryAlbum model
