
from pathlib import Path 
from .abc import ICollector
from .abc import BasePostPage 
from .utility import file_utility

class TaggedPostPage (BasePostPage):

  def __init__ (self, start: int, end: int, collector: ICollector, parent: ICollector, *, tag: str, config: dict):
    super().__init__(start, end, collector, parent, config=config)
    self.tag = tag

  def get_page_type (self):
    return "tag"

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    filename = file_utility.get_page_file(self.get_page_number(), config=self.get_config())
    return Path(dist_dir).joinpath("tag", self.tag.lower(), filename)

  def get_render_parameters (self):
    parameters = super().get_render_parameters()
    parameters["tag_group"] = self.tag
    return parameters
