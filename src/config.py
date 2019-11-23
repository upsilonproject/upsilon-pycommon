import argparse
import sys

def commonArgumentParser():
  parser = argparse.ArgumentParser();
  parser.add_argument('--server', '-s', help = "Hostname or IP address of upsilon-node", default = "upsilon")
  parser.add_argument('--port', '-p', help = "Port", default = 4000)
  parser.add_argument('--ssl', action = "store_true")
  parser.add_argument('--timeout', '-t', type = int, default = 10)
  parser.add_argument('--debug', '-d', action = 'store_true')

  return parser


