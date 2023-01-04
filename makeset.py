import argparse
from json import load
import logging
from math import floor
from os import makedirs
from os.path import join
from time import time
from makecard import make_unique_card

def make_set():
  pass

def save_set():
  pass

def parse_args():
  parser = argparse.ArgumentParser(description="a script to generate sets")

  parser.add_argument("--model", type=str, help='see readme')
  parser.add_argument("--set_template", type=str, default=join('config', 'set_v1.json'))
  # parser.add_argument("--output", type=str, default="print", choices=['print', 'save'])  # add 'both'?
  # parser.add_argument("--quantity", type=int, default="1")  # exclude?
  
  args = parser.parse_args()
  print(args)
  logging.debug(args)
  logging.info('arguments parsed')
  return args

def main():
  makedirs('./logs', exist_ok=True)
  logging.basicConfig(filename=join('logs', 'makeset.log'), encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()
  logging.info(f'attempting to make {arguments.quantity} set(s)')
  for i in range(arguments.quantity):
    logging.info(f'begin making set {i + 1} of {arguments.quantity}')
    # TODO(nyuu): rename this var, 'set' shadows the Python set type
    set = make_set(arguments)
    save_set(set)
  logging.info('ding!')


if __name__ == '__main__':
  main()