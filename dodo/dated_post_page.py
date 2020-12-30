
from pathlib import Path 
from .abc import ICollector 
from .abc import BasePostPage 
from .utility import file_utility

class DatedPostPage (BasePostPage):

  def __init__ (self, start: int, end: int, collector: ICollector, parent: ICollector, *, year: int, month: int=None, config: dict):
    super().__init__(start, end, collector, parent, config=config)
    self.year = year
    self.month = month 

  def get_page_type (self):
    return "date"

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    file = file_utility.get_page_file(self.get_page_number(), config=self.get_config())
    if self.month is not None:
      return Path(dist_dir).joinpath(str(self.year), str(self.month), file)
    else:
      return Path(dist_dir).joinpath(str(self.year), file)

  def get_render_parameters (self):
    parameters = super().get_render_parameters()
    parameters["date_group"] = { "year": self.year, "month": self.month }
    return parameters
