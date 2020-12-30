
template_classes = dict()

def make_template (*, config: dict):
  template_classname = config.get("template", dict()).get("class", "default")
  template_class = template_classes.get(template_classname)
  if template_class:
    return template_class(config=config)
  else:
    return None 
