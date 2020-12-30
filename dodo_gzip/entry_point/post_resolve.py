
import gzip
import shutil 
from io import IOBase
from pathlib import Path 
from dodo.abc import IConfigHolder 
from dodo.abc import BaseDependence 
from dodo.abc import IDistributable
from dodo.utility import file_utility
from dodo.cacheable_file import CacheableFile

def compress (path: Path, path_to: Path, compress_level: float):
  with CacheableFile(path, "rb").open() as instream:
    with gzip.open(path_to, "wb", compresslevel=round(compress_level * 9)) as outstream:
      shutil.copyfileobj(instream, outstream)

DEFAULT_COMPRESS_EXTENSIONS = {
  ".txt", ".html", ".css", ".js", ".json", ".xml"
}

def post_resolve (dependence: BaseDependence, forced: bool, *, log_stream: IOBase):
  if (isinstance(dependence, IConfigHolder) and 
      isinstance(dependence, IDistributable)):
    config = dependence.get_config()
    comperss_enable = config.get("gzip", dict()).get("enable", False)
    compress_level = config.get("gzip", dict()).get("compress_level", 1.0)
    compress_extensions = config.get("gzip", dict()).get("compress_extensions", DEFAULT_COMPRESS_EXTENSIONS)
    if comperss_enable:
      dist_file = dependence.get_dist_file()
      if dist_file.suffix in compress_extensions:
        compressed_file = dist_file.with_suffix(dist_file.suffix + ".gz")
        log_stream.write("compress to gzip => {}\n".format(compressed_file.as_posix())) #log
        compress(dist_file, compressed_file, compress_level)
