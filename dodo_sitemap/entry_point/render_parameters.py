
from dodo.abc import IConfigHolder
from dodo.abc import MixinRenderParameterHolder
from ..sitemap_collector import SitemapCollector  

def render_parameters (render_parameter_holder: MixinRenderParameterHolder):
  parameters = dict()
  if isinstance(render_parameter_holder, IConfigHolder):
    enable = render_parameter_holder.get_config().get("sitemap", dict()).get("enable", False)
    if enable:
      sitemap_collector = SitemapCollector(config=render_parameter_holder.get_config())
      sitemap_collector.collect()
      parameters.update(sitemap_collector.get_render_parameters())
  return parameters
