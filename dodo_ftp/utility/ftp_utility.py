
from io import IOBase
from ftplib import FTP
from pathlib import Path 
from dodo.utility import file_utility
from dodo.cacheable_file import CacheableFile

def make_dirs (path: Path, client: FTP, *, log_stream: IOBase=None):
  p = Path(path)
  if p.as_posix().startswith("/"):
    for i in range(1, len(p.parts)):
      dir = Path(*p.parts[0: i + 1])
      files = client.nlst(dir.parent.as_posix())
      if dir.name not in files:
        if log_stream:
          log_stream.write("mkd {}".format(dir.as_posix())) #log 
        client.mkd(dir.as_posix())
  else:
    raise ValueError("{} is must be absolute path.".format(p.as_posix()))

def upload_file (src: Path, dist: Path, client: FTP, *, log_stream: IOBase=None):
  s = Path(src)
  d = Path(dist)
  make_dirs(d.parent, client, log_stream=log_stream)
  with CacheableFile(s, "rb").open() as stream:
    if log_stream:
      log_stream.write("stor {}".format(d.as_posix())) #log 
    client.storbinary("STOR {}".format(d.as_posix()), stream)

def upload_newer_files (src_dir: Path, dist_dir: Path, newer_than: int, client: FTP, *, log_stream: IOBase=None):
  sdir = Path(src_dir)
  ddir = Path(dist_dir)
  for file in sdir.iterdir():
    next_src = sdir.joinpath(file.name)
    next_dist = ddir.joinpath(file.name)
    if next_src.is_file():
      if file_utility.is_newer(next_src, newer_than, when_does_not_exist=False):
        upload_file(next_src, next_dist, client, log_stream=log_stream)
    elif next_src.is_dir():
      upload_newer_files(next_src, next_dist, newer_than, client, log_stream=log_stream)
