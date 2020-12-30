
from io import IOBase, BytesIO
from pathlib import Path 
from xml.etree import ElementTree as etree
from dodo.abc import MixinPage
from dodo.abc import IDistributable
from dodo.abc import BaseDependence
from dodo.abc import ICollector 
from dodo.utility import url_utility
from dodo.utility import file_utility

DEFAULT_REGISTER_EXTENSIONS = {
  ".png", ".jpg", ".jpeg", ".gif", ".bmp",
  ".webp", ".svg",
}

class SitemapImage (MixinPage, IDistributable, BaseDependence):

  def __init__ (self, start: int, end: int, collector: ICollector, parent: ICollector, *, config: dict):
    super(BaseDependence, self).__init__()
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
    file = file_utility.get_numbered_file("sitemapimage{}.xml", self.get_page_number())
    return Path(dist_dir).joinpath(file)

  def should_resolve (self):
    for page_files in self.get_page_collection():
      if page_files.should_resolve() or any(( file_utility.is_older_than(self.get_dist_file(), file.get_dist_file(), when_does_not_exist=True) for file in page_files.get_collection() )):
        return True 
    return False 

  def render (self):
    register_extensions = self.get_config().get("sitemap_image", dict()).get("register_extensions", DEFAULT_REGISTER_EXTENSIONS)
    exlusive_files = self.get_config().get("sitemap_image", dict()).get("exlusive_files", set())
    xmlurlset = etree.Element("urlset")
    xmlurlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    xmlurlset.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")
    for page_files in self.get_page_collection():
      xmlurl = etree.SubElement(xmlurlset, "url")
      xmlloc = etree.SubElement(xmlurl, "loc")
      xmlloc.text = url_utility.make_absolute_http_url(page_files.page.get_dist_file().as_posix(), config=self.get_config())
      for file in page_files.get_collection():
        if file.get_dist_file().suffix in register_extensions:
          if not any(( file.get_dist_file().match(exlusive_file) for exlusive_file in exlusive_files )):
            xmlimage = etree.SubElement(xmlurl, "image:image")
            xmlimageloc = etree.SubElement(xmlurl, "image:loc")
            xmlimageloc.text = url_utility.make_absolute_http_url(file.get_dist_file().as_posix(), config=self.get_config())
    xmltree = etree.ElementTree(xmlurlset)
    with BytesIO() as buffer:
      xmltree.write(buffer, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
      return buffer.getvalue().decode("utf-8")

  def resolve (self, forced: bool, *, log_stream: IOBase):
    with file_utility.create_file_and_log(self.get_dist_file(), "w", encoding="utf-8", log_stream=log_stream) as stream:
      stream.write(self.render())
