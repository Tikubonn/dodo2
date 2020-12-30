
from io import IOBase 
from .icollector import ICollector 
from .base_dependence import BaseDependence

class BaseDependenceCollector (ICollector, BaseDependence):

  def should_resolve (self):
    for dependence in self.get_collection():
      if dependence.should_resolve():
        return True
    return False

  def resolve (self, forced: bool, *, log_stream: IOBase):
    for dependence in self.get_collection():
      dependence.try_resolve(forced, log_stream=log_stream)
