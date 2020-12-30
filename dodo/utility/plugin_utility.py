
import sys
import pkg_resources 

def get_ordered_entry_points (name, *, config: dict):
  plugin_order = config.get("plugin_order", list())
  return sorted(
    pkg_resources.iter_entry_points(name),
    key=lambda entry_point: plugin_order.index(entry_point.name) if entry_point.name in plugin_order else sys.maxsize
  )
