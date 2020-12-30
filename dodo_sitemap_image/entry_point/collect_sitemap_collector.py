
from ..sitemap_image_collector import SitemapImageCollector

def collect_sitemap_collector (*, config: dict):
  enable = config.get("sitemap_image", dict()).get("enable", False)
  if enable:
    sitemap_image_collector = SitemapImageCollector(config=config)
    sitemap_image_collector.collect()
    return sitemap_image_collector
  else:
    return None 
