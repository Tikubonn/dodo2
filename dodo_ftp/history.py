
import time 
import math 
import json 
import base64 
from io import IOBase
from pathlib import Path 
from hashlib import sha256
from dodo.utility import file_utility
from dodo.cacheable_file import CacheableFile

def get_history_filename (host: str, port: int, init_dir: str):
  source = "{}{}{}".format(host, port, init_dir).encode("utf-8")
  return base64.urlsafe_b64encode(sha256(source).digest()).decode("ascii") + ".json"

def get_history_file (host: str, port: int, init_dir: str, *, config: dict):
  cache_dir = config["cache_dir"]
  return Path(cache_dir).joinpath("ftp", get_history_filename(host, port, init_dir))

def get_last_modified (host: str, port: int, init_dir: str, *, config: dict):
  file = get_history_file(host, port, init_dir, config=config)
  if file.exists():
    with CacheableFile(file, "r", encoding="utf-8").open() as stream:
      return json.load(stream)
  else:
    return 0

def update_last_modified (host: str, port: int, init_dir: str, *, config: dict, log_stream: IOBase=None):
  file = get_history_file(host, port, init_dir, config=config)
  with file_utility.create_file_and_log(file, "w", encoding="utf-8", log_stream=log_stream) as stream:
    lastmod = math.floor(time.time())
    return json.dump(lastmod, stream)
