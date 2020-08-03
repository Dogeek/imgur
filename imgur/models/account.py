from imgur.models.base import Model


class Account(Model):
    def __init__(self, session, data=None):
        self.id = 0
        '''The account id for the username requested.'''
        self.url = ''
        '''The account username, will be the same as requested in the URL'''
        self.bio = ''
        '''A basic description the user has filled out'''
        self.reputation = 0.0
        '''The reputation for the account, in it's numerical format.'''
        self.created = 0
        '''The epoch time of account creation'''
        self.pro_expiration = False
        '''False if not a pro user, their expiration date if they are.'''

        super().__init__(session, data)


class MeAccount(Account):
    '''Represents the logged in user'''
