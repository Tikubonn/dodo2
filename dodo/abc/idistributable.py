
from abc import ABCMeta, abstractmethod

class IDistributable (metaclass=ABCMeta):
  
  @abstractmethod
  def get_dist_file (self):
    pass
