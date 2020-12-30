
import string 
from io import StringIO 
from dodo.abc import BaseHTMLTransformer

class HTMLMinifier (BaseHTMLTransformer):

  def __init__ (self):
    super().__init__()
    self.buffer = StringIO()

  def handle_data (self, text):
    lines = text.strip(string.whitespace).split("\n")
    joined = "\n".join(( line.strip(string.whitespace) for line in lines ))
    self.buffer.write(joined)

  def handle_comment (self, text):
    pass

def minify_html (text: str):
  minifier = HTMLMinifier()
  minifier.feed(text)
  return minifier.get_result()
