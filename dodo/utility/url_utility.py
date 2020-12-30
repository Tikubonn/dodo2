
from bs4 import BeautifulSoup as Bs
from urllib import parse as urlparse 
from pathlib import Path 
from ..abc.base_html_transformer import BaseHTMLTransformer

def make_absolute_url (url: str, *, config: dict):
  parsed = urlparse.urlparse(url)
  if parsed.scheme and parsed.netloc:
    return url
  if Path(parsed.path).is_absolute():
    return url
  if not Path(parsed.path).is_relative_to(config["dist_dir"]):
    return url
  path = Path("/").joinpath(Path(parsed.path).relative_to(config["dist_dir"]))
  return urlparse.urlunparse((
    parsed.scheme,
    parsed.netloc,
    urlparse.quote(path.as_posix()),
    parsed.params,
    parsed.query,
    parsed.fragment,
  ))

def make_absolute_http_url (url: str, *, config: dict):
  absolute_url = make_absolute_url(url, config=config)
  parsed = urlparse.urlparse(absolute_url)
  if parsed.scheme and parsed.netloc:
    return absolute_url
  use_ssl = config.get("use_ssl", False)
  if use_ssl:
    scheme = "https"
  else:
    scheme = "http"
  host = config.get("host", "example.com")
  return urlparse.urlunparse((
    scheme,
    parsed.netloc or host,
    parsed.path,
    parsed.params,
    parsed.query,
    parsed.fragment,
  ))

def make_absolute_url_for_post (url: str, post, *, config: dict):
  parsed = urlparse.urlparse(url)
  if parsed.scheme and parsed.netloc:
    return url
  if Path(parsed.path).is_absolute():
    return url
  creation_date = post.get_creation_date()
  path = Path("/", str(creation_date.year), str(creation_date.month), str(creation_date.day)).joinpath(parsed.path)
  return urlparse.urlunparse((
    parsed.scheme,
    parsed.netloc,
    urlparse.quote(path.as_posix()),
    parsed.params,
    parsed.query,
    parsed.fragment,
  ))

class HTMLURLFixer (BaseHTMLTransformer):

  def __init__ (self, post, fix_attributes):
    super().__init__()
    self.post = post
    self.fix_attributes = fix_attributes

  def handle_starttag (self, tag, attributes):
    super().handle_starttag(tag, (( key, make_absolute_url_for_post(value, self.post, config=self.post.get_config())) if key in self.fix_attributes else (key, value) for key, value in attributes ))

def fix_post_html (text, post, *, fix_attributes):
  html_url_fixer = HTMLURLFixer(post, fix_attributes)
  html_url_fixer.feed(text)
  return html_url_fixer.get_result()
