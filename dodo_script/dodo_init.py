
import os
import json 
import argparse 
from pathlib import Path 
from dodo.utility import file_utility

def main ():
  parser = argparse.ArgumentParser()
  parser.add_argument("--src-dir", type=Path, default=Path("src"))
  parser.add_argument("--dist-dir", type=Path, default=Path("dist"))
  parser.add_argument("--static-dir", type=Path, default=Path("static"))
  parser.add_argument("--cache-dir", type=Path, default=Path("cache"))
  parser.add_argument("--host", type=str, default="example.com")
  parser.add_argument("--use-ssl", action="store_true")
  parser.add_argument("--config-file", type=Path, default=Path("dodo.json"))
  parsed = parser.parse_args()
  os.makedirs(parsed.src_dir, exist_ok=True)
  os.makedirs(parsed.dist_dir, exist_ok=True)
  os.makedirs(parsed.static_dir, exist_ok=True)
  os.makedirs(parsed.cache_dir, exist_ok=True)
  with file_utility.create_file(parsed.config_file, "w", encoding="utf-8") as stream:
    config = {
      "src_dir": parsed.src_dir.as_posix(),
      "dist_dir": parsed.dist_dir.as_posix(),
      "static_dir": parsed.static_dir.as_posix(),
      "cache_dir": parsed.cache_dir.as_posix(),
      "host": parsed.host,
      "use_ssl": parsed.use_ssl,
    }
    json.dump(config, stream, ensure_ascii=False, indent=2, sort_keys=True)
