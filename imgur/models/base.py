class Model:
    def __init__(self, session, data=None):
        self.session = session
        '''ImgurSession instance'''
        self._data = None
        '''The data for this model, as a dict'''

        if isinstance(data, dict):
            self.set(**data)

    def set(self, **data):
        '''
        Set this models attributes according to the values of **data
        '''
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def dict(self):
        '''
        Returns a dictionnary of this model

        :return: Dictionnary of this model
        :rtype: dict
        '''
        return {k: v for k, v in zip(self.__data.keys(), [getattr(self, k) for k in self._data])}

    @property
    def json(self):
        '''
        JSON string of the model

        :return: A JSON serialized string of the model
        :rtype: str
        '''
        return self.session.json.dumps(self.dict)
