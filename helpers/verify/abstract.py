from abc import ABC, abstractmethod

class Abstract(ABC):
    """
    验证器抽象类
    """
    @abstractmethod
    def same_shape(self, **kwargs):
        pass

    @abstractmethod
    def slide(self, **kwargs):
        pass