
from io import IOBase
from ..sitemap_collector import SitemapCollector 

def update (forced: bool, *, config: dict, log_stream: IOBase):
  enable = config.get("sitemap", dict()).get("enable", False)
  if enable:
    sitemap_collector = SitemapCollector(config=config)
    sitemap_collector.collect()
    sitemap_collector.try_resolve(forced, log_stream=log_stream)
