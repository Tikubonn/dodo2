
from io import IOBase
from .abc import ICollector
from .abc import BaseDependence
from .file_collector import FileCollector

class StaticFileCollector (ICollector, BaseDependence):

  def __init__ (self, *, config: dict, exclusive_files: set=set()):
    super(BaseDependence, self).__init__()
    self.config = dict(config)
    self.exclusive_files = set(exclusive_files)
    self.file_collector = None 

  def get_config (self):
    return self.config

  def get_exclusive_files (self):
    exclusive_files = set()
    exclusive_files.update(self.exclusive_files)
    exclusive_files.update(self.get_config().get("static", dict()).get("exclusives", set()))
    return exclusive_files

  def get_collection (self):
    if self.file_collector:
      return self.file_collector.get_collection()
    else:
      return list()

  def collect (self):
    self.file_collector = FileCollector(
      self.get_config()["static_dir"], 
      self.get_config()["dist_dir"], 
      config=self.get_config(), 
      exclusive_files=self.get_exclusive_files()
    )
    self.file_collector.collect()

  def should_resolve (self):
    if self.file_collector:
      if self.file_collector.should_resolve():
        return True 
    return False 

  def resolve (self, forced: bool, *, log_stream: IOBase):
    if self.file_collector:
      self.file_collector.resolve(forced, log_stream=log_stream)
