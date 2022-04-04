from easyai.other_modules import SingletonClass

class UpdateClass(SingletonClass):

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
