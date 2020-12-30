
from .abc import ICollector 

class Collector (ICollector):

  def __init__ (self):
    self.collection = list()

  def get_collection (self):
    return self.collection

  def collect (self, collection):
    self.collection = collection

  def append (self, item):
    self.collection.append(item)
