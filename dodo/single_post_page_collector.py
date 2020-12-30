
from .abc import BasePageCollector
from .post_collector import PostCollector
from .single_post_page import SinglePostPage 

class SinglePostPageCollector (BasePageCollector):

  def __init__ (self, *, config: dict):
    super(BasePageCollector, self).__init__()
    self.config = config
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def collect (self):
    post_collector = PostCollector(config=self.get_config())
    post_collector.collect()
    self.collection.clear()
    for i in range(len(post_collector.get_collection())):
      page = SinglePostPage(i, i+1, post_collector, self, config=self.get_config())
      self.collection.append(page)
