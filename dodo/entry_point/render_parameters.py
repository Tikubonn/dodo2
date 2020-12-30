
from ..abc import IConfigHolder 
from ..abc import MixinRenderParameterHolder
from ..dated_post_page_collector import DatedPostPageCollector 
from ..recent_post_page_collector import RecentPostPageCollector 
from ..tagged_post_page_collector import TaggedPostPageCollector 

def render_parameters (render_parameter_holder: MixinRenderParameterHolder):
  parameters = dict()
  if isinstance(render_parameter_holder, IConfigHolder):
    if render_parameter_holder.get_config().get("page", dict()).get("use_dated_page_parameter", False):
      date_post_page_collector = DatedPostPageCollector(config=render_parameter_holder.get_config())
      date_post_page_collector.collect()
      parameters.update(date_post_page_collector.get_render_parameters())
    if render_parameter_holder.get_config().get("page", dict()).get("use_recent_page_parameter", False):
      recent_post_page_collector = RecentPostPageCollector(config=render_parameter_holder.get_config())
      recent_post_page_collector.collect()
      parameters.update(recent_post_page_collector.get_render_parameters())
    if render_parameter_holder.get_config().get("page", dict()).get("use_tagged_page_parameter", False):
      tagged_post_page_collector = TaggedPostPageCollector(config=render_parameter_holder.get_config())
      tagged_post_page_collector.collect()
      parameters.update(tagged_post_page_collector.get_render_parameters())
  return parameters
