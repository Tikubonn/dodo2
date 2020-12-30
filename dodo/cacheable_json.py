
import json 
from pathlib import Path 
from .cacheable_file import CacheableFile 

class CacheableJSON (CacheableFile):

  cached_data = None 

  def reload (self):
    super().reload()
    self.cached_data = json.loads(self.cached_content)

  def load (self):
    self.try_reload()
    return self.cached_data
