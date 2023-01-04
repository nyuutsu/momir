from argparse import ArgumentParser, Namespace
import logging
from math import floor
from os import makedirs
from os.path import join
from time import time

import openai
import requests

def make_card(args: Namespace) -> dict:
  return dict(openai.Completion.create(
    model=args.model,
    prompt=f"{args.supertype} ->",
    max_tokens=250,
    temperature=1,
    best_of=1,
    stop="ꙮ"
  ))['choices'][0]['text']

def make_unique_card(args: Namespace) -> dict:
  """rejection sampling wrapper for make_card
  TODO: add "scryfall is down" & "too many failures" exit conditions"""
  fail_count = 0
  while True:
    card = make_card(args)
    card_name = card.split('\n')[:1][0].split(':')[1].strip()
    petition = requests.get(f'https://api.scryfall.com/cards/named?pretty=true&exact={card_name}').json()
    if petition['object'] == 'error':
      logging.info(f'ok: {card_name}. returning')
      return card
    fail_count += 1
    logging.info(f'collision: {card_name}. collisions: {fail_count}. retrying')

def save_card(card: str, timestamp: str) -> None:
  with open(join('output', f'Cards_{timestamp}.txt'), 'a', encoding='utf-8') as file:
    file.write(card)
  pass

def output_card(card: str, arguments: Namespace, timestamp: str) -> None:
  if arguments.output == 'save':
    save_card(card, timestamp)
  else:
    logging.info(f'mode: console output:\n{card}')
    print(card)

def parse_args() -> Namespace:
  parser = ArgumentParser(description="a script to generate cards")

  parser.add_argument("--model", type=str, help='see readme')
  parser.add_argument("--supertype", type=str, default="creature", choices=['creature', 'instant', 'sorcery', 'land', 'enchantment', 'artifact', 'planeswalker', 'tribal'])
  parser.add_argument("--output", type=str, default="print", choices=['print', 'save'])
  parser.add_argument("--quantity", type=int, default="1")
  
  args = parser.parse_args()
  print(args)
  logging.debug(args)
  logging.info('arguments seem parsed')
  return args

def main() -> None:
  makedirs('./logs', exist_ok=True)
  logging.basicConfig(filename=join('logs', 'makecard.log'), encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()
  logging.info('beginning run')
  timestamp = floor(time())
  for _ in range(arguments.quantity):
    card = make_unique_card(arguments)
    output_card(card, arguments, timestamp)
  logging.info('ending run')

if __name__ == '__main__':
  main()