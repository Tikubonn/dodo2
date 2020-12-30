
import time 
import multiprocessing 
from multiprocessing import Process

class Pool:

  def __init__ (self, max_process_count: int=multiprocessing.cpu_count()):
    self.max_process_count = max_process_count
    self.working_processes = list()

  def __enter__ (self):
    return self

  def __exit__ (self, error_type, error_value, backtrace):
    if error_value and error_type and backtrace:
      self.abort()
    else:
      self.wait()

  def abort (self):
    for process in self.working_processes[:]:
      process.kill()
      self.wait_for_free_process.remove(process)

  def wait (self, timeout: int=None):
    for process in self.working_processes[:]:
      process.join(timeout)
      if not process.is_alive():
        self.working_processes.remove(process)

  def wait_for_free_process (self):
    while not len(self.working_processes) < self.max_process_count:
      self.wait(0)
      time.sleep(0)

  def run (self, function, *args, **kwargs):
    self.wait_for_free_process()
    process = Process(target=function, args=args, kwargs=kwargs)
    process.start()
    self.working_processes.append(process)
