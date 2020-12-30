
from pathlib import Path 
from .abc import BasePostPage 

class SinglePostPage (BasePostPage):

  def get_post (self):
    return self.get_page_collection()[0]

  def get_page_type (self):
    return "single"

  def get_dist_file (self):
    dist_dir = self.get_config()["dist_dir"]
    post = self.get_post()
    creation_date = post.get_creation_date()
    file = self.get_config().get("index_file", "index.html")
    return Path(dist_dir).joinpath(
      str(creation_date.year), 
      str(creation_date.month), 
      str(creation_date.day), 
      file
    )

  def get_render_parameters (self):
    parameters = super().get_render_parameters()
    parameters["post"] = self.get_post().get_render_parameters()
    return parameters
