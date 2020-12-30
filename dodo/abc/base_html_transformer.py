
from io import StringIO 
from html.parser import HTMLParser

class BaseHTMLTransformer (HTMLParser):

  def __init__ (self):
    super().__init__()
    self.buffer = StringIO()

  def handle_starttag (self, tag, attributes):
    self.buffer.write("<")
    self.buffer.write(tag)
    for key, value in attributes:
      self.buffer.write(" ")
      self.buffer.write(key)
      self.buffer.write("=\"")
      self.buffer.write(value)
      self.buffer.write("\"")
    self.buffer.write(">")

  def handle_endtag (self, tag):
    self.buffer.write("</")
    self.buffer.write(tag)
    self.buffer.write(">")

  def handle_startendtag (self, tag, attributes):
    self.handle_starttag(tag, attributes)

  def handle_data (self, text):
    self.buffer.write(text)

  def handle_entityref (self, text):
    self.buffer.write("&")
    self.buffer.write(text)
    self.buffer.write(";")

  def handle_charref (self, text):
    self.buffer.write("&#")
    self.buffer.write(text)
    self.buffer.write(";")

  def handle_comment (self, text):
    self.buffer.write("<!-- ")
    self.buffer.write(text)
    self.buffer.write(" -->")

  def handle_decl (self, text):
    self.buffer.write("<!")
    self.buffer.write(text)
    self.buffer.write(">")

  def get_result (self):
    return self.buffer.getvalue()
