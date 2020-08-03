class Controller:
    """Base class for imgur controllers"""
    def __init__(self, session):
        self.session = session

    def __call__(self, *args, **kwargs):
        return getattr(
            self,
            self.__class__.__name__.split('Controller')[0].lower()
        )(*args, **kwargs)
