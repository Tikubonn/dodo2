
from ..post import Post 
from ..utility import url_utility 

def post_get_summary_text (post: Post, text: str):
  return url_utility.fix_post_html(text, post, fix_attributes=[ "src", "href" ])
