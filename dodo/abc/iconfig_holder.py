
from abc import ABCMeta, abstractmethod 

class IConfigHolder (metaclass=ABCMeta):

  @abstractmethod
  def get_config (self):
    pass
