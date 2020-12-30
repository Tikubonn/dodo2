
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as stream:
  long_description = stream.read()

setup(
  name="dodo2",
  description="a builder and CMS tools for static web-log.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  version="0.1.0",
  license="GPLv3",
  author="tikubonn",
  author_email="https://twitter.com/tikubonn",
  url="https://github.com/tikubonn/dodo2",
  packages=find_packages(exclude=["demo"]),
  install_requires=[
    "bs4",
    "html5lib",
    "jinja2",
  ],
  dependency_links=[],
  entry_points={
    "console_scripts": [
      "dodo=dodo_script.dodo:main",
      "dodo-init=dodo_script.dodo_init:main",
      "dodo-create=dodo_script.dodo_create:main",
      "dodo-update=dodo_script.dodo_update:main",
    ],
    "dodo.init": [
      "dodo_jinja2=dodo_jinja2.entry_point:init",
    ],
    "dodo.post_get_full_text": [
      "dodo=dodo.entry_point:post_get_full_text",
    ],
    "dodo.post_get_summary_text": [
      "dodo=dodo.entry_point:post_get_summary_text",
    ],
    "dodo.render_parameters": [
      "dodo=dodo.entry_point:render_parameters",
      "dodo_sitemap=dodo_sitemap.entry_point:render_parameters",
      "dodo_sitemap_image=dodo_sitemap_image.entry_point:render_parameters",
      "dodo_sitemap_index=dodo_sitemap_index.entry_point:render_parameters",
    ],
    "dodo.update": [
      "dodo_script=dodo_script.entry_point:update",
      "dodo_ftp=dodo_ftp.entry_point:update",
      "dodo_sitemap=dodo_sitemap.entry_point:update",
      "dodo_sitemap_image=dodo_sitemap_image.entry_point:update",
      "dodo_sitemap_index=dodo_sitemap_index.entry_point:update",
    ],
    "dodo.collect_sitemap_collector": [
      "dodo_sitemap=dodo_sitemap.entry_point:collect_sitemap_collector",
      "dodo_sitemap_image=dodo_sitemap_image.entry_point:collect_sitemap_collector",
    ],
    "dodo.post_resolve": [
      "dodo_gzip=dodo_gzip.entry_point:post_resolve",
      "dodo_minify_html=dodo_minify_html.entry_point:post_resolve",
      "dodo_minify_css=dodo_minify_css.entry_point:post_resolve",
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
  ]
)
