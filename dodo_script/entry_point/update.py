
from io import IOBase
from dodo import StaticFileCollector 
from dodo import DatedPostPageCollector 
from dodo import TaggedPostPageCollector 
from dodo import RecentPostPageCollector 
from dodo import SinglePostPageCollector 
from dodo import SinglePostPageFilesCollector 

def update (forced: bool, *, config: dict, log_stream: IOBase):
  static_file_collector = StaticFileCollector(config=config)
  static_file_collector.collect()
  static_file_collector.try_resolve(forced, log_stream=log_stream)
  single_post_page_collector = SinglePostPageCollector(config=config)
  single_post_page_collector.collect()
  single_post_page_collector.try_resolve(forced, log_stream=log_stream)
  single_post_page_files_collector = SinglePostPageFilesCollector(config=config)
  single_post_page_files_collector.collect()
  single_post_page_files_collector.try_resolve(forced, log_stream=log_stream)
  recent_post_page_collector = RecentPostPageCollector(config=config)
  recent_post_page_collector.collect()
  recent_post_page_collector.try_resolve(forced, log_stream=log_stream)
  dated_post_page_collector = DatedPostPageCollector(config=config)
  dated_post_page_collector.collect()
  dated_post_page_collector.try_resolve(forced, log_stream=log_stream)
  tagged_post_page_collector = TaggedPostPageCollector(config=config)
  tagged_post_page_collector.collect()
  tagged_post_page_collector.try_resolve(forced, log_stream=log_stream)
