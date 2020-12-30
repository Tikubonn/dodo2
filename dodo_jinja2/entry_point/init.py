
from ..template_jinja2 import TemplateJinja2
from dodo import template_maker 

def init ():
  template_maker.template_classes.setdefault("default", TemplateJinja2)
  template_maker.template_classes["jinja2"] = TemplateJinja2
