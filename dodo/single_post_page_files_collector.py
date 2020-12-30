
from .abc import BaseDependenceCollector
from .single_post_page_files import SinglePostPageFiles 
from .single_post_page_collector import SinglePostPageCollector

class SinglePostPageFilesCollector (BaseDependenceCollector):

  def __init__ (self, *, config: dict, exclusive_files: set=set()):
    super(BaseDependenceCollector, self).__init__()
    self.config = config
    self.exclusive_files = exclusive_files
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def collect (self):
    single_post_page_collector = SinglePostPageCollector(config=self.get_config())
    single_post_page_collector.collect()
    self.collection.clear()
    for page in single_post_page_collector.get_collection():
      page_files = SinglePostPageFiles(page, config=self.get_config())
      page_files.collect()
      self.collection.append(page_files)
