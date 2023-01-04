from argparse import ArgumentParser, Namespace
from json import load
import logging
from math import floor
from os import makedirs
from os.path import join
from time import time

from makecard import make_unique_card

def make_deck(args: Namespace) -> list:
  deck = []
  with open(join('config', args.deck_template)) as file:
    template = load(file)
  for supertype_key, supertype_value in enumerate(template['generated']):
    for _ in range(supertype_value['uniques']):
      deck.append(f"quantity {supertype_value['copies']} {make_unique_card(supertype_key)[1:]}")
      logging.info('generated card created')
  for deckstring in template['static']:
    deck.append(deckstring)
    logging.info('static card added')
  return deck

def save_deck(deck: list) -> None:
  timestamp = floor(time())
  logging.info(f'mode: file output "Deck_{timestamp}.txt":\n{deck}')
  with open(f'Deck_{timestamp}.txt', 'a') as file:
    for card in deck:      
      file.write(f'{card}\n')

def output_deck(deck: list, arguments: Namespace) -> None:
  if arguments.output == 'save':
    save_deck(list)
  else:
    logging.info(f'mode: console output:\n{deck}')
    print(deck)
  
def parse_args() -> Namespace:
  parser = ArgumentParser(description="a script to generate decks")

  parser.add_argument("--model", type=str, help='see readme')
  parser.add_argument("--deck_template", type=str, default=join('config', 'deck_template_v1.json'))
  parser.add_argument("--output", type=str, default="print", choices=['print', 'save'])
  parser.add_argument("--quantity", type=int, default="1")
  
  args = parser.parse_args()
  print(args)
  logging.debug(args)
  logging.info('arguments parsed')
  return args

def main() -> None:
  makedirs('./logs', exist_ok=True)
  logging.basicConfig(filename=join('logs', 'makedeck.log'), encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()
  logging.info(f'attempting to make {arguments.quantity} decks')
  for i in range(arguments.quantity):
    logging.info(f'begin making deck {i}')
    deck = make_deck(arguments)
    output_deck(deck, arguments)
  logging.info('ding!')

if __name__ == '__main__':
  main()