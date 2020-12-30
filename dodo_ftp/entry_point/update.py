
from io import IOBase
from ftplib import FTP, FTP_TLS
from .. import history
from ..utility import ftp_utility

def apply_updates (*, server_config: dict, config: dict, log_stream: IOBase):
  host = server_config.get("host")
  port = server_config.get("port", 21)
  init_dir = server_config.get("init_dir", "/")
  user = server_config.get("user", "anonymous")
  save_password = server_config.get("save_password", False)
  use_ssl = server_config.get("use_ssl", False)
  key_file = server_config.get("key_file", None)
  cert_file = server_config.get("cert_file", None)
  lastmod = history.get_last_modified(host, port, init_dir, config=config)
  if use_ssl:
    ftp = FTP_TLS(keyfile=key_file, certfile=cert_file)
    ftp.connect(host, port)
    ftp.login(user=user)
    ftp.prot_p()
  else:
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(user=user)
  dist_dir = config["dist_dir"]
  ftp_utility.upload_newer_files(dist_dir, init_dir, lastmod, ftp, log_stream=log_stream)
  ftp.quit()
  ftp.close()
  history.update_last_modified(host, port, init_dir, config=config, log_stream=log_stream)

def update (forced: bool, *, config: dict, log_stream: IOBase):
  server_configs = config.get("ftp", dict()).get("servers", list())
  for server_config in server_configs:
    try: 
      apply_updates(server_config=server_config, config=config, log_stream=log_stream)
    except ConnectionError as error:
      print("ConnectionError:", error)
