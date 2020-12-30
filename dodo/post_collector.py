
from .abc import ICollector
from .abc import IConfigHolder
from .post import Post 
from pathlib import Path 

class PostCollector (IConfigHolder, ICollector):

  def __init__ (self, *, config: dict):
    self.config = config
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def collect (self):
    src_dir = Path(self.get_config()["src_dir"])
    self.collection.clear()
    for file in src_dir.iterdir():
      if file.is_dir():
        post = Post(file, config=self.get_config())
        self.collection.append(post)
    self.collection.sort(key=lambda post: post.get_creation_date(), reverse=True)
