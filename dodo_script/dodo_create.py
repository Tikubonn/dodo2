
import os 
import sys 
import json 
import argparse 
from pathlib import Path 
from datetime import datetime
from dodo import Post 

def main ():
  parser = argparse.ArgumentParser()
  parser.add_argument("id", type=str)
  parser.add_argument("--summary-text", type=str, default="")
  parser.add_argument("--full-text", type=str, default="")
  parser.add_argument("--title", type=str, default="")
  parser.add_argument("--description", type=str, default="")
  parser.add_argument("--keywords", nargs="+", default=list())
  parser.add_argument("--tags", nargs="+", default=list())
  parser.add_argument("--quiet", action="store_true")
  parser.add_argument("--config-file", type=Path, default="dodo.json")
  parsed = parser.parse_args()
  os.chdir(parsed.config_file.parent)
  with open(parsed.config_file, "r", encoding="utf-8") as stream:
    config = json.load(stream)
  src_dir = config["src_dir"]
  post_dir = Path(src_dir).joinpath(parsed.id)
  if parsed.quiet:
    log_stream = open(os.devnull, "w") 
  else:
    log_stream = sys.stdout
  post = Post(post_dir, config=config)
  now = datetime.now()
  post_config = {
    "title": parsed.title,
    "description": parsed.description,
    "keywords": parsed.keywords,
    "tags": parsed.tags,
    "creation_date": {
      "year": now.year,
      "month": now.month,
      "day": now.day,
      "hour": now.hour,
      "minute": now.minute,
      "second": now.second,
    }
  }
  post.create(
    summary_text=parsed.summary_text, 
    full_text=parsed.full_text, 
    post_config=post_config, 
    log_stream=log_stream
  )
