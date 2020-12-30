
from .abc import BasePageCollector
from .abc import MixinRenderParameterHolder
from .collector import Collector
from .dated_post_page import DatedPostPage
from .single_post_page_collector import SinglePostPageCollector

class DatedPostPageCollector (MixinRenderParameterHolder, BasePageCollector):

  def __init__ (self, *, config: dict):
    super(BasePageCollector, self).__init__()
    self.config = config
    self.year_single_pages = dict()
    self.year_pages = dict()
    self.year_month_single_pages = dict()
    self.year_month_pages = dict()

  def get_config (self):
    return self.config

  def get_collection (self):
    collection = list()
    for pages in self.year_pages.values():
      collection.extend(pages)
    for month_pages in self.year_month_pages.values():
      for pages in month_pages.values():
        collection.extend(pages)
    return collection

  def collect (self):
    single_post_page_collector = SinglePostPageCollector(config=self.get_config())
    single_post_page_collector.collect()
    year_single_pages = dict()
    year_month_single_pages = dict()
    for page in single_post_page_collector.get_collection():
      post = page.get_post()
      creation_date = post.get_creation_date()
      year_single_pages.setdefault(creation_date.year, list())
      year_single_pages.get(creation_date.year).append(page)
      year_month_single_pages.setdefault(creation_date.year, dict())
      year_month_single_pages.get(creation_date.year).setdefault(creation_date.month, list())
      year_month_single_pages.get(creation_date.year).get(creation_date.month).append(page)
    post_count_per_page = self.get_config().get("post_count_per_page", 10)
    year_pages = dict()
    for year, pages in year_single_pages.items():
      collector = Collector()
      collector.collect([ page.get_post() for page in pages ])
      page_collector = Collector()
      for i in range(0, len(pages), post_count_per_page):
        page = DatedPostPage(i, i + post_count_per_page, collector, page_collector, year=year, config=self.get_config())
        page_collector.append(page)
        year_pages.setdefault(year, list())
        year_pages.get(year).append(page)
    year_month_pages = dict()
    for year, month_pages in year_month_single_pages.items():
      for month, pages in month_pages.items():
        collector = Collector()
        collector.collect([ page.get_post() for page in pages ])
        page_collector = Collector()
        for i in range(0, len(pages), post_count_per_page):
          page = DatedPostPage(i, i + post_count_per_page, collector, page_collector, year=year, month=month, config=self.get_config())
          page_collector.append(page)
          year_month_pages.setdefault(year, dict())
          year_month_pages.get(year).setdefault(month, list())
          year_month_pages.get(year).get(month).append(page)
    self.year_single_pages = year_single_pages
    self.year_pages = year_pages
    self.year_month_single_pages = year_month_single_pages
    self.year_month_pages = year_month_pages

  def get_render_parameters (self):
    parameters = dict()
    parameters["year_single_pages"] = { year: [ page.get_render_parameters() for page in pages ] for year, pages in self.year_single_pages.items() }
    parameters["year_pages"] = { year: [ page.get_render_parameters() for page in pages ] for year, pages in self.year_pages.items() }
    parameters["year_month_single_pages"] = { year: { month: [ page.get_render_parameters() for page in pages ] for month, pages in month_pages.items() } for year, month_pages in self.year_month_single_pages.items() }
    parameters["year_month_pages"] = { year: { month: [ page.get_render_parameters() for page in pages ] for month, pages in month_pages.items() } for year, month_pages in self.year_month_pages.items() }
    return parameters
