
from io import IOBase
from abc import ABCMeta, abstractmethod 
from .iconfig_holder import IConfigHolder
from ..utility import plugin_utility

class BaseDependence (IConfigHolder, metaclass=ABCMeta):

  @abstractmethod
  def should_resolve (self):
    pass

  @abstractmethod
  def resolve (self, forced: bool, *, log_stream: IOBase):
    pass

  def pre_resolve (self, forced: bool, *, log_stream: IOBase):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.pre_resolve", config=self.get_config()):
      entry_point.load()(self, forced, log_stream=log_stream)

  def post_resolve (self, forced: bool, *, log_stream: IOBase):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.post_resolve", config=self.get_config()):
      entry_point.load()(self, forced, log_stream=log_stream)

  def try_resolve (self, forced: bool=False, *, log_stream: IOBase):
    if forced or self.should_resolve():
      self.pre_resolve(forced, log_stream=log_stream)
      self.resolve(forced, log_stream=log_stream)
      self.post_resolve(forced, log_stream=log_stream)
