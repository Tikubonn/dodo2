
from io import IOBase, BytesIO
from pathlib import Path 
from xml.etree import ElementTree as etree
from dodo.abc import MixinPage
from dodo.abc import ICollector
from dodo.abc import BaseDependence
from dodo.abc import IDistributable
from dodo.utility import url_utility
from dodo.utility import file_utility

class Sitemap (MixinPage, IDistributable, BaseDependence):

  def __init__ (self, start: int, end: int, collector: ICollector, parent: ICollector, *, config: dict):
    self.start = start
    self.end = end
    self.collector = collector
    self.parent = parent
    self.config = config

  def get_page_start (self):
    return self.start

  def get_page_end (self):
    return self.end

  def get_page_collector (self):
    return self.collector

  def get_page_parent (self):
    return self.parent

  def get_config (self):
    return self.config

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    file = file_utility.get_numbered_file("sitemap{}.xml", self.get_page_number())
    return Path(dist_dir).joinpath(file)

  def render (self):
    xmlurlset = etree.Element("urlset")
    xmlurlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for page in self.get_page_collection():
      post = page.get_post()
      post_config = post.get_post_config()
      xmlurl = etree.SubElement(xmlurlset, "url")
      xmlloc = etree.SubElement(xmlurl, "loc")
      xmlloc.text = url_utility.make_absolute_http_url(page.get_dist_file().as_posix(), config=self.get_config())
      xmllastmod = etree.SubElement(xmlurl, "lastmod")
      xmllastmod.text = post.get_last_modified_date().date().isoformat()
      changefreq = post_config.get("changefreq")
      if changefreq:
        xmlchangefreq = etree.SubElement(xmlurl, "changefreq")
        xmlchangefreq.text = changefreq
      priority = post_config.get("priority")
      if priority:
        xmlpriority = etree.SubElement(xmlurl, "priority")
        xmlpriority.text = priority
    xmltree = etree.ElementTree(xmlurlset)
    with BytesIO() as buffer:
      xmltree.write(buffer, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
      return buffer.getvalue().decode("utf-8")

  def should_resolve (self):
    for page in self.get_page_collection():
      if file_utility.is_older_than(self.get_dist_file(), page.get_dist_file(), when_does_not_exist=True):
        return True 
    return False 

  def resolve (self, forced: bool, *, log_stream: IOBase):
    with file_utility.create_file_and_log(self.get_dist_file(), "w", encoding="utf-8", log_stream=log_stream) as stream:
      stream.write(self.render())
