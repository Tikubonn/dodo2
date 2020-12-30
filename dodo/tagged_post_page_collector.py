
from pathlib import Path 
from .abc import BasePageCollector
from .abc import MixinRenderParameterHolder
from .collector import Collector 
from .tagged_post_page import TaggedPostPage
from .single_post_page_collector import SinglePostPageCollector

class TaggedPostPageCollector (MixinRenderParameterHolder, BasePageCollector):

  def __init__ (self, *, config: dict):
    super(BasePageCollector, self).__init__()
    self.config = config
    self.tagged_single_pages = dict()
    self.tagged_pages = dict()

  def get_config (self):
    return self.config

  def get_collection (self):
    collection = list()
    for pages in self.tagged_pages.values():
      collection.extend(pages)
    return collection

  def collect (self):
    single_post_page_collector = SinglePostPageCollector(config=self.get_config())
    single_post_page_collector.collect()
    tagged_single_pages = dict()
    tagged_single_posts = dict()
    for page in single_post_page_collector.get_collection():
      post = page.get_post()
      for tag in post.get_post_config().get("tags", set()):
        tagged_single_pages.setdefault(tag, list())
        tagged_single_pages.get(tag).append(page)
        tagged_single_posts.setdefault(tag, list())
        tagged_single_posts.get(tag).append(post)
    post_count_per_page = self.get_config().get("post_count_per_page", 10)
    tagged_pages = dict()
    for tag, posts in tagged_single_posts.items():
      collector = Collector()
      collector.collect(posts)
      page_collector = Collector()
      for i in range(0, len(posts), post_count_per_page):
        page = TaggedPostPage(i, i + post_count_per_page, collector, page_collector, tag=tag, config=self.get_config())
        page_collector.append(page)
        tagged_pages.setdefault(tag, list())
        tagged_pages.get(tag).append(page)
    self.tagged_single_pages = tagged_single_pages
    self.tagged_pages = tagged_pages

  def get_render_parameters (self):
    parameters = dict()
    parameters["tagged_single_pages"] = { tag: [ page.get_render_parameters() for page in pages ] for tag, pages in self.tagged_single_pages.items() }
    parameters["tagged_pages"] = { tag: [ page.get_render_parameters() for page in pages ] for tag, pages in self.tagged_pages.items() }
    return parameters
