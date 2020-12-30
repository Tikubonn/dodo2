
from io import IOBase
from ..sitemap_index import SitemapIndex 

def update (forced: bool, *, config: dict, log_stream: IOBase):
  enable = config.get("sitemap_index", dict()).get("enable", False)
  if enable:
    sitemap_index = SitemapIndex(config=config)
    sitemap_index.collect()
    sitemap_index.try_resolve(forced, log_stream=log_stream)
