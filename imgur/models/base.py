class Model:
    def __init__(self, session, data=None):
        self.session = session
        if isinstance(data, dict):
            self.set(**data)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
