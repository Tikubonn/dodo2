
from abc import ABCMeta, abstractmethod
from .iconfig_holder import IConfigHolder 
from ..utility import plugin_utility 

class MixinRenderParameterHolder (metaclass=ABCMeta):

  @abstractmethod
  def get_render_parameters (self):
    pass

  def get_full_render_parameters (self):
    if isinstance(self, IConfigHolder):
      parameters = self.get_render_parameters()
      for entry_point in plugin_utility.get_ordered_entry_points("dodo.render_parameters", config=self.get_config()):
        parameters.update(entry_point.load()(self))
      return parameters
    else:
      raise TypeError("{} must inherit {}.", MixinRenderParameterHolder.__name__, IConfigHolder.__name__)
