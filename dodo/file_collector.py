
from pathlib import Path 
from .abc import BaseDependenceCollector
from .file import File 

class FileCollector (BaseDependenceCollector):

  def __init__ (self, src: Path, dist: Path, *, config: dict, exclusive_files: set=set()):
    super(BaseDependenceCollector, self).__init__()
    self.src = Path(src)
    self.dist = Path(dist)
    self.config = config
    self.exclusive_files = set(exclusive_files)
    self.collection = list()

  def get_config (self):
    return self.config

  def get_exclusive_files (self):
    exclusive_files = set()
    exclusive_files.update(self.exclusive_files)
    exclusive_files.update(self.get_config().get("file", dict()).get("exclusives", set()))
    return exclusive_files

  def get_collection (self):
    return self.collection

  def collect_at (self, src: Path, dist: Path):
    s = Path(src)
    d = Path(dist)
    for file in s.iterdir():
      next_src = s.joinpath(file.name)
      next_dist = d.joinpath(file.name)
      if next_src.is_file():
        if not any((next_src.match(str(exclusive)) for exclusive in self.get_exclusive_files())):
          file = File(next_src, next_dist, config=self.get_config())
          self.collection.append(file)
      else:
        self.collect_at(next_src, next_dist)

  def collect (self):
    self.collection.clear()
    self.collect_at(self.src, self.dist)
