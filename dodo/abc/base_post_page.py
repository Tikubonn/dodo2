
import json 
from io import IOBase 
from abc import ABCMeta, abstractmethod 
from pathlib import Path 
from .. import template_maker 
from ..utility import url_utility 
from ..utility import file_utility 
from .mixin_page import MixinPage
from .icollector import ICollector
from .idistributable import IDistributable
from .base_dependence import BaseDependence
from .mixin_render_parameter_holder import MixinRenderParameterHolder

class BasePostPage (IDistributable, MixinPage, MixinRenderParameterHolder, BaseDependence, metaclass=ABCMeta):

  def __init__ (self, start: int, end: int, collector: ICollector, parent: ICollector, *, config: dict):
    super(BaseDependence, self).__init__()
    self.start = start
    self.end = end
    self.collector = collector
    self.parent = parent
    self.config = config

  def get_page_start (self):
    return self.start

  def get_page_end (self):
    return self.end

  def get_page_collector (self):
    return self.collector

  def get_page_parent (self):
    return self.parent

  def get_config (self):
    return self.config

  def get_full_render_parameters (self):
    parameters = super().get_full_render_parameters()
    parameters["next_pages"] = [ page.get_render_parameters() for page in self.get_next_pages() ]
    parameters["previous_pages"] = [ page.get_render_parameters() for page in self.get_previous_pages() ]
    next_page = self.get_next_page()
    if next_page:
      parameters["next_page"] = next_page.get_render_parameters()
    else:
      parameters["next_page"] = None 
    previous_page = self.get_previous_page()
    if previous_page:
      parameters["previous_page"] = previous_page.get_render_parameters()
    else:
      parameters["previous_page"] = None 
    return parameters

  def get_render_parameters (self):
    parameters = dict()
    parameters["posts"] = [ post.get_render_parameters() for post in self.get_page_collection() ]
    parameters["page_number"] = self.get_page_number()
    parameters["page_type"] = self.get_page_type()
    parameters["url"] = url_utility.make_absolute_url(self.get_dist_file().as_posix(), config=self.get_config())
    parameters["full_url"] = url_utility.make_absolute_http_url(self.get_dist_file().as_posix(), config=self.get_config())
    return parameters

  @abstractmethod
  def get_page_type (self):
    pass

  def make_template (self):
    return template_maker.make_template(config=self.get_config())

  def should_resolve (self):
    template = template_maker.make_template(config=self.get_config())
    if template:
      if file_utility.is_older(self.get_dist_file(), template.get_last_modified(), when_does_not_exist=True):
        return True 
    for post in self.get_page_collection():
      if file_utility.is_older(self.get_dist_file(), post.get_last_modified(), when_does_not_exist=True):
        return True 
    return  False

  def resolve (self, forced: bool, *, log_stream: IOBase):
    template = template_maker.make_template(config=self.get_config())
    if template:
      parameters = self.get_full_render_parameters()
      with file_utility.create_file_and_log(self.get_dist_file(), "w", encoding="utf-8", log_stream=log_stream) as stream:
        stream.write(template.render(parameters))
