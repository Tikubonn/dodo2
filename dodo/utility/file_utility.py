
import os 
import shutil 
from io import IOBase
from pathlib import Path 
from multiprocessing import Lock

def create_file (path: Path, *args, **kwargs):
  p = Path(path)
  os.makedirs(p.parent, exist_ok=True)
  return open(p, *args, **kwargs)

def copy_file (path: Path, path_to: Path):
  p = Path(path)
  pto = Path(path_to)
  os.makedirs(pto.parent, exist_ok=True)
  shutil.copyfile(p, pto)

def create_file_and_log (path: Path, *args, log_stream: IOBase, **kwargs):
  log_stream.write("create => {}\n".format(Path(path).as_posix())) #log
  return create_file(path, *args, **kwargs)

def copy_file_and_log (path: Path, path_to: Path, log_stream: IOBase):
  log_stream.write("copy {} => {}\n".format(Path(path).as_posix(), Path(path_to).as_posix())) #log
  return copy_file(path, path_to)

def is_older (path: Path, than: int, when_does_not_exist: bool=False):
  p = Path(path)
  if p.is_file():
    return p.stat().st_mtime < than
  else:
    return when_does_not_exist

def is_newer (path: Path, than: int, when_does_not_exist: bool=False):
  p = Path(path)
  if p.is_file():
    return than < p.stat().st_mtime
  else:
    return when_does_not_exist

def is_older_than (path: Path, path_than: Path, when_does_not_exist: bool=False):
  p = Path(path)
  pthan = Path(path_than)
  if p.is_file() and pthan.is_file():
    return p.stat().st_mtime < pthan.stat().st_mtime
  else:
    return when_does_not_exist

def get_numbered_file (format: str, page_number: int):
  if 1 < page_number:
    return format.format(page_number)
  else:
    return format.format("")

def get_page_file (page_number: int, *, config: dict):
  if 1 < page_number:
    return config.get("page_file", "page{}.html").format(page_number)
  else:
    return config.get("index_file", "index.html")
