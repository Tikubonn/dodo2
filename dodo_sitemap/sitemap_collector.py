
from dodo import SinglePostPageCollector 
from dodo.abc import BasePageCollector
from dodo.abc import MixinRenderParameterHolder 
from dodo.utility import url_utility
from .sitemap import Sitemap

class SitemapCollector (MixinRenderParameterHolder, BasePageCollector):

  def __init__ (self, *, config: dict):
    self.config = config
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def collect (self):
    single_post_page_collector = SinglePostPageCollector(config=self.get_config())
    single_post_page_collector.collect()
    pages = single_post_page_collector.get_collection()
    post_count_per_sitemap = self.get_config().get("sitemap", dict()).get("post_count_per_sitemap", 1000)
    self.collection.clear()
    for i in range(0, len(pages), post_count_per_sitemap):
      sitemap = Sitemap(i, i + post_count_per_sitemap, single_post_page_collector, self, config=self.get_config())
      self.collection.append(sitemap)

  def get_render_parameters (self):
    parameters = dict()
    parameters["sitemap_urls"] = [ url_utility.make_absolute_url(sitemap.get_dist_file().as_posix(), config=self.get_config()) for sitemap in self.get_collection() ]
    return parameters
