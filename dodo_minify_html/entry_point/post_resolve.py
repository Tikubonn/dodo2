
from io import IOBase, StringIO 
from bs4 import BeautifulSoup as Bs
from dodo.abc import IConfigHolder 
from dodo.abc import IDistributable
from dodo.abc import BaseDependence
from .. import html_minifier

def post_resolve (dependence: BaseDependence, forced: bool, *, log_stream: IOBase):
  if (isinstance(dependence, IConfigHolder) and 
      isinstance(dependence, IDistributable)):
    enable = dependence.get_config().get("minify_html", dict()).get("enable", False)
    target_extensions = dependence.get_config().get("minify_html", dict()).get("target_extensions", [ ".html" ])
    if enable:
      dist_file = dependence.get_dist_file()
      if dist_file.suffix in target_extensions:
        log_stream.write("minify html => {}\n".format(dist_file.as_posix())) #log
        with open(dist_file, "r", encoding="utf-8") as stream:
          source = stream.read()
        with open(dist_file, "w", encoding="utf-8") as stream:
          minified = html_minifier.minify_html(source)
          stream.write(minified)
