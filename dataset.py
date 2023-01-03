import argparse
import logging
from json import load
from os.path import exists as file_exists
from requests import get as rget

def get_scryfall_data() -> None:
  url = 'https://api.scryfall.com/bulk-data'
  reqs = rget(url, timeout=1).json()['data'][0]['download_uri']
  with open('cardlist.json', 'wb') as file:
    file.write(rget(reqs).content)
  
def check_if_keep(card: dict, filters: list) -> bool:
  """old approach to curating cardpool (w/ filters.json)"""
  if 'card_faces' in card:
    return False
  return all(card[criteria[0]] != criteria[1] for criteria in filters)

def in_format(card: dict, format: str) -> bool:
  return card['legalities'][format] != 'not_legal'

def remove_unneeded_attributes(cardpool, args):
  with open('unneeded_attributes.json') as file:
    unneeded_attributes = load(file)
  with open('unneeded_attributes_low.json') as file:
    potentially_unneeded_attributes = load(file)

  for card in cardpool:
    for attribute in unneeded_attributes:
      if attribute in card:
        del card[attribute]
    
    if args.granularity == 'low':
      for attribute in potentially_unneeded_attributes:
        if attribute in card:
          del card[attribute]
  
def generate_training_data(args, filename: str = 'cardlist.json'):
  with open(filename) as file:
    cards = load(file)

  if args.file_filter:
    with open(args.file_filter) as file:
      file_filter = file.readlines()
      file_filter = [card.strip() for card in file_filter]
    cardpool = [card for card in cards if card['name'] in file_filter]
  elif args.format_filter:
    cardpool = [card for card in cards if in_format(card, args.format_filter)]

  remove_unneeded_attributes(cardpool, args)
  
  with open('training_data.jsonl', 'w') as file:
    for card in cardpool:
      card_data = ""
      for attribute, value in card.items():
        if attribute != 'cmc' and attribute != 'colors':
          card_data += attribute + ": " + str(value).replace("\"", "\'") + "\n"
      card_data = card_data.replace("\n", "\\n")
      if args.granularity == 'low':
        file.write(f'{{"prompt":"{card["type_line"].split()[0]} ->","completion":" {card_data}ꙮ"}}\n')
      else:
        file.write(f'{{"prompt":"CMC {int(card["cmc"])} {card["colors"]} {card["type_line"].split()[0]} ->","completion":" {card_data}ꙮ"}}\n')
    print(f'# created: {len(cardpool)}')

def parse_args():
  parser=argparse.ArgumentParser(description="a script to prepare a dataset for training. only one filter flag is considered.")
  parser.add_argument("--file_filter", type=str, help='provide a filename for filter')
  parser.add_argument("--format_filter", type=str, default="legacy")
  parser.add_argument("--granularity", type=str, choices=['high', 'low'], default='low', help='set to high if you want to specify color and cmc')
  args=parser.parse_args()
  return args

def main() -> None:
  logging.basicConfig(filename='scrape.log', encoding='utf-8', level=logging.DEBUG)

  arguments = parse_args()  

  if not file_exists('cardlist.json'):
    get_scryfall_data()

  if file_exists('cardlist.json'):
    generate_training_data(arguments)

if __name__ == '__main__':
  main()