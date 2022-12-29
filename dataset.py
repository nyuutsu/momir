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
  if card['legalities'][format] == 'not_legal':
    return False
  return True

def generate_training_data(filename: str = 'cardlist.json', format='legacy'):
  with open(filename) as file:
    cards = load(file)
  
  format_cardpool = [card for card in cards if in_format(card, format)]

  with open('unneeded_attributes.json') as file:
    unneeded_attributes = load(file)

  for card in format_cardpool:
    for attribute in unneeded_attributes:
      try:
        del card[attribute]
      except KeyError:
        pass  # some cards don't have, e.g. flavor text, to remove.

  with open('training_data.jsonl', 'w') as file:
    for card in format_cardpool:
      card_data = ""
      for attribute, value in card.items():
        card_data += attribute + ": " + str(value).replace("\"", "\'") + "\n"
      card_data = card_data.replace("\n", "\\n")
      file.write(f'{{"prompt":"{card["type_line"].split()[0]} ->","completion":" {card_data}ꙮ"}}\n')
    print(f'# created: {len(format_cardpool)}')

def main() -> None:
  if not file_exists('cardlist.json'):
    get_scryfall_data()

  if file_exists('cardlist.json'):
    generate_training_data()
  
if __name__ == '__main__':
  main()