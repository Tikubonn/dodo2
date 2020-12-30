
from abc import ABCMeta, abstractmethod 

class ICollector (metaclass=ABCMeta):

  @abstractmethod
  def get_collection (self):
    pass

  @abstractmethod
  def collect (self):
    pass
