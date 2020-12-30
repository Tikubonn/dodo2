
from dodo.abc import IConfigHolder
from dodo.abc import MixinRenderParameterHolder
from ..sitemap_index import SitemapIndex  

def render_parameters (render_parameter_holder: MixinRenderParameterHolder):
  parameters = dict()
  if isinstance(render_parameter_holder, IConfigHolder):
    enable = render_parameter_holder.get_config().get("sitemap_index", dict()).get("enable", False)
    if enable:
      sitemap_index = SitemapIndex(config=render_parameter_holder.get_config())
      sitemap_index.collect()
      parameters.update(sitemap_index.get_render_parameters())
  return parameters
