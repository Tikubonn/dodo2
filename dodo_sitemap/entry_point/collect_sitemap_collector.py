
from ..sitemap_collector import SitemapCollector 

def collect_sitemap_collector (*, config: dict):
  enable = config.get("sitemap", dict()).get("enable", False)
  if enable:
    sitemap_collector = SitemapCollector(config=config)
    sitemap_collector.collect()
    return sitemap_collector
  else:
    return None 
