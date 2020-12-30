
import time 
from io import BytesIO, StringIO
from pathlib import Path 
from weakref import WeakValueDictionary

class CacheableFile:

  instances = WeakValueDictionary()
  cached_content = None 
  cached_time = 0

  def __new__ (self, path: Path, mode: str, *args, **kwargs):
    key = (Path(path), mode)
    instance = super(CacheableFile, self).__new__(self)
    self.instances.setdefault(key, instance)
    return self.instances.get(key, instance)

  def __init__ (self, path: Path, mode: str, *args, **kwargs):
    self.path = Path(path)
    self.mode = mode
    self.args = args
    self.kwargs = kwargs

  def get_path (self):
    return self.path 

  def should_reload (self):
    return self.cached_time < self.path.stat().st_mtime

  def reload (self):
    with open(self.path, self.mode, *self.args, **self.kwargs) as stream:
      self.cached_content = stream.read()
      self.cached_time = time.time()

  def try_reload (self):
    if self.should_reload():
      self.reload()

  def read (self):
    self.try_reload()
    return self.cached_content

  def open (self):
    self.try_reload()
    if self.cached_content:
      if isinstance(self.cached_content, bytes):
        return BytesIO(self.cached_content)
      elif isinstance(self.cached_content, str):
        return StringIO(self.cached_content)
      else:
        raise TypeError()
    else:
      raise ValueError()
