
import argparse 
import subprocess

def main ():
  parser = argparse.ArgumentParser()
  parser.add_argument("subcommand", type=str)
  parser.add_argument("arguments", nargs=argparse.REMAINDER)
  parsed = parser.parse_args()
  subprocess.run([ "dodo-{}".format(parsed.subcommand) ] + list(parsed.arguments), check=True)
