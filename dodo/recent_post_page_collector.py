
from .abc import BasePageCollector
from .abc import MixinRenderParameterHolder
from .post_collector import PostCollector
from .recent_post_page import RecentPostPage
from .single_post_page_collector import SinglePostPageCollector

class RecentPostPageCollector (MixinRenderParameterHolder, BasePageCollector):

  def __init__ (self, *, config: dict):
    super(BasePageCollector, self).__init__()
    self.config = config
    self.recent_single_pages = list()
    self.recent_pages = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.recent_pages

  def collect (self):
    post_collector = PostCollector(config=self.get_config())
    post_collector.collect()
    post_count_per_page = self.get_config().get("post_count_per_page", 10)
    self.recent_pages.clear()
    for i in range(0, len(post_collector.get_collection()), post_count_per_page):
      page = RecentPostPage(i, i + post_count_per_page, post_collector, self, config=self.get_config())
      self.recent_pages.append(page)
    single_post_page_collector = SinglePostPageCollector(config=self.get_config())
    single_post_page_collector.collect()
    self.recent_single_pages.clear()
    self.recent_single_pages.extend(single_post_page_collector.get_collection())

  def get_render_parameters (self):
    parameters = dict()
    parameters["recent_single_pages"] = [ page.get_render_parameters() for page in self.recent_single_pages ]
    parameters["recent_pages"] = [ page.get_render_parameters() for page in self.recent_pages ]
    return parameters
