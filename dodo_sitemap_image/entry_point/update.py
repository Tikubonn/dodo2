
from io import IOBase
from ..sitemap_image_collector import SitemapImageCollector

def update (forced: bool, *, config: dict, log_stream: IOBase):
  enable = config.get("sitemap_image", dict()).get("enable", False)
  if enable:
    sitemap_image_collector = SitemapImageCollector(config=config)
    sitemap_image_collector.collect()
    sitemap_image_collector.try_resolve(forced, log_stream=log_stream)
