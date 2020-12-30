
import json 
from io import IOBase
from pathlib import Path 
from datetime import datetime
from .abc import IConfigHolder
from .abc import MixinRenderParameterHolder
from .utility import file_utility
from .utility import plugin_utility
from .cacheable_file import CacheableFile
from .cacheable_json import CacheableJSON

class Post (IConfigHolder, MixinRenderParameterHolder):

  def __init__ (self, path: Path, *, config: dict):
    self.path = Path(path)
    self.config = config
    self.cached_full_text_file = self.make_cached_full_text_file()
    self.cached_summary_text_file = self.make_cached_summary_text_file()
    self.cached_post_config_json = self.make_cached_post_config_json()

  def get_config (self):
    return self.config

  def make_cached_full_text_file (self):
    file = self.get_config().get("post", dict()).get("full_text_file", "full_text.html")
    return CacheableFile(self.path.joinpath(file), "r", encoding="utf-8")

  def make_cached_summary_text_file (self):
    file = self.get_config().get("post", dict()).get("summary_text_file", "summary_text.html")
    return CacheableFile(self.path.joinpath(file), "r", encoding="utf-8")

  def make_cached_post_config_json (self):
    file = self.get_config().get("post", dict()).get("post_config_file", "config.json")
    return CacheableJSON(self.path.joinpath(file), "r", encoding="utf-8")

  def get_full_text_file (self):
    return self.cached_full_text_file.get_path()

  def get_summary_text_file (self):
    return self.cached_summary_text_file.get_path()

  def get_post_config_file (self):
    return self.cached_post_config_json.get_path()

  def post_get_full_text (self, text):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.post_get_full_text", config=self.get_config()):
      text = entry_point.load()(self, text)
    return text

  def post_get_summary_text (self, text):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.post_get_summary_text", config=self.get_config()):
      text = entry_point.load()(self, text)
    return text

  def get_full_text (self):
    with self.cached_full_text_file.open() as stream:
      full_text = stream.read()
      return self.post_get_full_text(full_text)

  def get_summary_text (self):
    with self.cached_summary_text_file.open() as stream:
      summary_text = stream.read()
      return self.post_get_summary_text(summary_text)

  def get_post_config (self):
    return self.cached_post_config_json.load()

  def get_last_modified (self):
    return max(
      self.get_full_text_file().stat().st_mtime,
      self.get_summary_text_file().stat().st_mtime,
      self.get_post_config_file().stat().st_mtime
    )

  def get_last_modified_date (self):
    return datetime.fromtimestamp(self.get_last_modified())

  def get_creation_date (self):
    post_config = self.get_post_config()
    return datetime(
      post_config["creation_date"]["year"],
      post_config["creation_date"]["month"],
      post_config["creation_date"]["day"],
      post_config["creation_date"]["hour"],
      post_config["creation_date"]["minute"],
      post_config["creation_date"]["second"]
    )

  def get_render_parameters (self):
    parameters = dict()
    parameters.update(self.get_post_config())
    parameters["full_text"] = self.get_full_text()
    parameters["summary_text"] = self.get_summary_text()
    creation_date = self.get_creation_date()
    parameters["creation_date"] = {
      "year": creation_date.year,
      "month": creation_date.month,
      "day": creation_date.day,
      "hour": creation_date.hour,
      "minute": creation_date.minute,
      "second": creation_date.second,
    }
    last_modified_date = self.get_last_modified_date()
    parameters["last_modified_date"] = {
      "year": last_modified_date.year,
      "month": last_modified_date.month,
      "day": last_modified_date.day,
      "hour": last_modified_date.hour,
      "minute": last_modified_date.minute,
      "second": last_modified_date.second,
    }
    return parameters

  def post_create (self, *, summary_text: str, full_text: str, post_config: dict, log_stream: IOBase):
    for entry_point in plugin_utility.get_ordered_entry_points("dodo.post_create", config=self.get_config()):
      entry_point.load()(self, summary_text=summary_text, full_text=full_text, post_config=post_config, log_stream=log_stream)

  def create (self, *, summary_text: str, full_text: str, post_config: dict, log_stream: IOBase):
    if not self.path.exists():
      with file_utility.create_file_and_log(self.get_summary_text_file(), "w", log_stream=log_stream) as stream:
        stream.write(summary_text)
      with file_utility.create_file_and_log(self.get_full_text_file(), "w", log_stream=log_stream) as stream:
        stream.write(full_text)
      with file_utility.create_file_and_log(self.get_post_config_file(), "w", log_stream=log_stream) as stream:
        json.dump(post_config, stream, ensure_ascii=False, indent=2, sort_keys=True)
      self.post_create(summary_text=summary_text, full_text=full_text, post_config=post_config, log_stream=log_stream)
