class Model:
    def __init__(self, session, data=None):
        self.session = session
        init()
        if isinstance(data, dict):
            self.set(**data)

    def init(self):
        raise NotImplementedError()

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
