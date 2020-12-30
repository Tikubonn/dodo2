
from pathlib import Path 
from .abc import BasePostPage
from .utility import file_utility

class RecentPostPage (BasePostPage):

  def get_page_type (self):
    return "recent"

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    file = file_utility.get_page_file(self.get_page_number(), config=self.get_config())
    return Path(dist_dir).joinpath(file)
