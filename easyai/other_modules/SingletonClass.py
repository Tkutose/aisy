from abc import ABCMeta, abstractmethod

class SingletonClass(metaclass=ABCMeta):
    _instance = None

