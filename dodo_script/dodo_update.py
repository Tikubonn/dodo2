
import os 
import sys
import json 
import argparse 
from pathlib import Path 
from dodo.utility import plugin_utility

def main ():
  parser = argparse.ArgumentParser()
  parser.add_argument("--always-update", action="store_true")
  parser.add_argument("--quiet", action="store_true")
  parser.add_argument("--config-file", type=Path, default=Path("dodo.json"))
  parsed = parser.parse_args()
  os.chdir(parsed.config_file.parent)
  with open(parsed.config_file, "r", encoding="utf-8") as stream:
    config = json.load(stream)
  if parsed.quiet:
    log_stream = open(os.devnull, "w")
  else:
    log_stream = sys.stdout
  for entry_point in plugin_utility.get_ordered_entry_points("dodo.update", config=config):
    entry_point.load()(parsed.always_update, config=config, log_stream=log_stream)
