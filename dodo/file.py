
from io import IOBase
from pathlib import Path 
from .abc import BaseDependence
from .abc import IDistributable
from .utility import file_utility 

class File (IDistributable, BaseDependence):

  def __init__ (self, src: Path, dist: Path, *, config: dict):
    super(BaseDependence, self).__init__()
    self.src = Path(src)
    self.dist = Path(dist)
    self.config = config

  def get_dist_file (self):
    return self.dist

  def get_config (self):
    return self.config

  def should_resolve (self):
    return file_utility.is_older_than(self.dist, self.src, when_does_not_exist=True)

  def resolve (self, forced: bool, *, log_stream: IOBase):
    file_utility.copy_file_and_log(self.src, self.dist, log_stream=log_stream)
