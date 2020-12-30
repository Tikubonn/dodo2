
from io import IOBase
from .icollector import ICollector 
from .base_dependence import BaseDependence

class BasePageCollector (ICollector, BaseDependence):

  def where_should_resolve (self):
    for i, page in enumerate(self.get_collection()):
      if page.should_resolve():
        return i 
    return -1

  def should_resolve (self):
    i = self.where_should_resolve()
    return 0 <= i

  def resolve (self, forced: bool, *, log_stream: IOBase):
    if forced:
      i = 0
    else:
      i = self.where_should_resolve()
    if 0 <= i:
      for page in self.get_collection()[i:]:
        page.try_resolve(True, log_stream=log_stream)
