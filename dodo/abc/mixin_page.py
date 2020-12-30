
from abc import ABCMeta, abstractmethod 

class MixinPage (metaclass=ABCMeta):

  @abstractmethod
  def get_page_start (self):
    pass

  @abstractmethod
  def get_page_end (self):
    pass

  @abstractmethod
  def get_page_collector (self):
    pass

  @abstractmethod
  def get_page_parent (self):
    pass

  def get_page_collection (self):
    return self.get_page_collector().get_collection()[self.get_page_start(): self.get_page_end()]

  def get_page_index (self):
    return self.get_page_parent().get_collection().index(self)

  def get_page_number (self):
    return self.get_page_index() +1

  def get_next_pages (self):
    return self.get_page_parent().get_collection()[:self.get_page_index()]

  def get_previous_pages (self):
    return self.get_page_parent().get_collection()[self.get_page_index() +1:]

  def get_next_page (self):
    pages = self.get_next_pages()
    if pages:
      return pages[-1]
    else:
      return None 

  def get_previous_page (self):
    pages = self.get_previous_pages()
    if pages:
      return pages[0]
    else:
      return None 
