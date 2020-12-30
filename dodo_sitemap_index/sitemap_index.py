
from io import IOBase, BytesIO
from pathlib import Path 
from xml.etree import ElementTree as etree
from dodo.abc import ICollector
from dodo.abc import BaseDependence
from dodo.abc import IDistributable
from dodo.abc import MixinRenderParameterHolder 
from dodo.utility import url_utility
from dodo.utility import file_utility
from dodo.utility import plugin_utility

class SitemapIndex (ICollector, MixinRenderParameterHolder, IDistributable, BaseDependence):

  def __init__ (self, *, config: dict):
    super(BaseDependence, self).__init__()
    self.config = config
    self.collection = list()

  def get_config (self):
    return self.config

  def get_collection (self):
    return self.collection

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    return Path(dist_dir).joinpath("sitemapindex.xml")

  def should_resolve (self):
    for sitemap in self.get_collection():
      if sitemap.should_resolve() or file_utility.is_older_than(self.get_dist_file(), sitemap.get_dist_file(), when_does_not_exist=True):
        return True 
    return False 

  def render (self):
    xmlsitemapindex = etree.Element("sitemapindex")
    xmlsitemapindex.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for sitemap in self.get_collection():
      xmlsitemap = etree.SubElement(xmlsitemapindex, "sitemap")
      xmlloc = etree.SubElement(xmlsitemap, "loc")
      xmlloc.text = url_utility.make_absolute_http_url(sitemap.get_dist_file().as_posix(), config=self.get_config())
    xmltree = etree.ElementTree(xmlsitemapindex)
    with BytesIO() as buffer:
      xmltree.write(buffer, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
      return buffer.getvalue().decode("utf-8")

  def resolve (self, forced: bool, *, log_stream: IOBase):
    with file_utility.create_file_and_log(self.get_dist_file(), "w", encoding="utf-8", log_stream=log_stream) as stream:
      stream.write(self.render())

  def collect_sitemap (self):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.collect_sitemap", config=self.get_config()):
      sitemap = entry_point.load()(config=self.get_config())
      if sitemap:
        self.collection.append(sitemap)

  def collect_sitemap_collector (self):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.collect_sitemap_collector", config=self.get_config()):
      sitemap_collector = entry_point.load()(config=self.get_config())
      if sitemap_collector:
        self.collection.extend(sitemap_collector.get_collection())

  def collect (self):
    self.collect_sitemap()
    self.collect_sitemap_collector()

  def get_render_parameters (self):
    parameters = dict()
    parameters["sitemapindex_url"] = url_utility.make_absolute_url(self.get_dist_file().as_posix(), config=self.get_config())
    return parameters
