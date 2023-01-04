import argparse
import logging
from math import floor
import openai
from os import makedirs
from os.path import join
import requests
from time import time

def make_card(args) -> dict:
  return dict(openai.Completion.create(
    model=args.model,
    prompt=f"{args.supertype} ->",
    max_tokens=250,
    temperature=1,
    #top_p=0.5,
    best_of=1,
    stop="ꙮ"
  ))['choices'][0]['text']

def make_unique_card(args) -> dict:
  """rejection sampling wrapper for make_card
  TODO: add "scryfall is down" & "too many failures" exit conditions"""

  while True:
    card = make_card(args)
    card_name = card.split('\n')[:1][0].split(':')[1].strip()
    petition = requests.get(f'https://api.scryfall.com/cards/named?pretty=true&exact={card_name}').json()
    if petition['object'] == 'error':
      logging.info(f'card name ok: {card_name}; returning')
      return card
    logging.info(f'card name collision: {card_name}; retrying')

def make_deck() -> list:
  """
  return a list containing a deck. deck consists of 60 card strings.
  a card string consists of card quantity & rules text
  decks have 12 creatures, 8 sorceries, 8 instants, 2 artifacts,
  2 enchantments, 2 planeswalkers, and 26 lands.
  10 lands are predetermined, preexisting rainbow lands.
  """
  deck = []
  
  for _ in range(3):
    deck.append("quantity 4\n" + make_unique_card('Creature')[1:])
  for _ in range(2):
    deck.append("quantity 4\n" + make_unique_card('Sorcery')[1:])
  for _ in range(2):
    deck.append("quantity 4\n" + make_unique_card('Instant')[1:])
  for _ in range(1):
    deck.append("quantity 2\n" + make_unique_card('Artifact')[1:])
  for _ in range(1):
    deck.append("quantity 2\n" + make_unique_card('Enchantment')[1:])
  for _ in range(1):
    deck.append("quantity 2\n" + make_unique_card('Planeswalker')[1:])
  for _ in range(4):
    deck.append("quantity 4\n" + make_unique_card('Land')[1:])
  
  deck.append("quantity 4\n" + "name: Mana Confluence\nmana_cost: \ntype_line: Land\noracle_text: {T}, Pay 1 life: Add one mana of any color.\n")

  deck.append("quantity 4\n" + "name: City of Brass\nmana_cost: \ntype_line: Land\noracle_text: Whenever City of Brass becomes tapped, it deals 1 damage to you.\n{T}: Add one mana of any color.\n")

  deck.append("quantity 2\n" + "name: Gemstone Mine\nmana_cost: \ntype_line: Land\noracle_text: Gemstone Mine enters the battlefield with three mining counters on it.\n{T}, Remove a mining counter from Gemstone Mine: Add one mana of any color. If there are no mining counters on Gemstone Mine, sacrifice it.\n")

  return deck

def save_deck(deck: list) -> None:
  with open(f'Deck_{floor(time())}.txt', 'a') as file:
    for card in deck:      
      file.write(f'{card}\n')

def parse_args():
  parser = argparse.ArgumentParser(description="a script to generate cards and decks'")

  parser.add_argument("--model", type=str, help='see readme')
  parser.add_argument("--supertype", type=str, default="creature", choices=['creature', 'instant', 'sorcery', 'land', 'enchantment', 'artifact', 'planeswalker', 'tribal'])
  parser.add_argument("--deck", type=str, default="false", choices=['true', 'false'])
  parser.add_argument("--deck_template", type=str, default="default")
  parser.add_argument("--output", type=str, default="print", choices=['print', 'save'])
  parser.add_argument("--quantity", type=int, default="1")
  
  args = parser.parse_args()
  print(args)
  logging.debug(args)
  logging.info('arguments seem parsed')
  return args

def main():
  makedirs('./logs', exist_ok=True)
  logging.basicConfig(filename=join('logs', 'maker.log'), encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()
  logging.info('beginning run')
  for _ in range(arguments.quantity):
    card = make_unique_card(arguments)
    print(card)
  logging.info('ending run')

if __name__ == '__main__':
  main()