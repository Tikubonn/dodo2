
from dodo import SinglePostPageFilesCollector
from dodo.abc import MixinRenderParameterHolder
from dodo.abc import BasePageCollector
from dodo.utility import url_utility
from .sitemap_image import SitemapImage

class SitemapImageCollector (MixinRenderParameterHolder, BasePageCollector):

  def __init__ (self, *, config: dict):
    super(BasePageCollector, self).__init__()
    self.config = config
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def collect (self):
    single_post_page_files_collector = SinglePostPageFilesCollector(config=self.get_config())
    single_post_page_files_collector.collect()
    post_count_per_sitemap = self.get_config().get("sitemap_image", dict()).get("post_count_per_sitemap", 1000)
    self.collection.clear()
    for i in range(0, len(single_post_page_files_collector.get_collection()), post_count_per_sitemap):
      sitemap = SitemapImage(i, i + post_count_per_sitemap, single_post_page_files_collector, self, config=self.get_config())
      self.collection.append(sitemap)

  def get_render_parameters (self):
    parameters = dict()
    parameters["sitemap_image_urls"] = [ url_utility.make_absolute_http_url(sitemap.get_dist_file().as_posix(), config=self.get_config()) for sitemap in self.get_collection() ]
    return parameters
