
from jinja2 import Template 
from pathlib import Path 
from dodo.abc import BaseTemplate 
from dodo.cacheable_file import CacheableFile

class TemplateJinja2 (BaseTemplate):

  def __init__ (self, *, config: dict):
    super().__init__()
    self.config = config

  def get_config (self):
    return self.config

  def get_template_file (self):
    template_file = self.get_config().get("template", dict())["src"]
    return Path(template_file)

  def get_last_modified (self):
    return self.get_template_file().stat().st_mtime

  def render (self, parameters: dict):
    template_file = self.get_template_file()
    with CacheableFile(template_file, "r", encoding="utf-8").open() as stream:
      template = Template(stream.read())
      return template.render(**parameters)
