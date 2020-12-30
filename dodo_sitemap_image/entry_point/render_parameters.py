
from dodo.abc import IConfigHolder
from dodo.abc import MixinRenderParameterHolder
from ..sitemap_image_collector import SitemapImageCollector  

def render_parameters (render_parameter_holder: MixinRenderParameterHolder):
  parameters = dict()
  if isinstance(render_parameter_holder, IConfigHolder):
    enable = render_parameter_holder.get_config().get("sitemap_image", dict()).get("enable", False)
    if enable:
      sitemap_image_collector = SitemapImageCollector(config=render_parameter_holder.get_config())
      sitemap_image_collector.collect()
      parameters.update(sitemap_image_collector.get_render_parameters())
  return parameters
