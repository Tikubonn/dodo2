
from abc import ABCMeta, abstractmethod 
from .iconfig_holder import IConfigHolder 

class BaseTemplate (IConfigHolder, metaclass=ABCMeta):

  @abstractmethod
  def get_last_modified (self):
    pass

  @abstractmethod
  def render (self, parameters: dict):
    pass
