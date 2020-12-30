
from .abc import BaseDependenceCollector
from .file_collector import FileCollector
from .single_post_page import SinglePostPage

class SinglePostPageFiles (BaseDependenceCollector):

  def __init__ (self, page: SinglePostPage, *, config: dict, exclusive_files: set=set()):
    super(BaseDependenceCollector, self).__init__()
    self.page = page
    self.config = config
    self.exclusive_files = exclusive_files
    self.file_collector = None 

  def get_config (self):
    return self.config

  def get_collection (self):
    if self.file_collector:
      return self.file_collector.get_collection()
    else:
      return list()

  def collect (self):
    exclusive_files = set()
    exclusive_files.update({
      self.page.get_post().get_summary_text_file(),
      self.page.get_post().get_full_text_file(),
      self.page.get_post().get_post_config_file(),
    })
    exclusive_files.update(self.exclusive_files)
    file_collector = FileCollector(self.page.get_post().path, self.page.get_dist_file().parent, config=self.get_config(), exclusive_files=exclusive_files)
    file_collector.collect()
    self.file_collector = file_collector
