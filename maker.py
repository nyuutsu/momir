from math import floor
from time import time
import openai

def make_card(supertype: str) -> dict:
  return dict(openai.Completion.create(
    model="davinci:ft-personal-2022-12-27-16-32-43",
    prompt=f"{supertype} ->",
    max_tokens=250,
    temperature=1,
    stop="ꙮ"
  ))['choices'][0]['text']

def make_deck() -> list:
  """
  return a list containing a deck. deck consists of 60 card strings.
  a card string consists of card quantity & rules text
  decks have 12 creatures, 8 sorceries, 8 instants, 2 artifacts,
  2 enchantments, 2 planeswalkers, and 26 lands.
  10 lands are predetermined, preexisting rainbow lands.
  """
  deck = []
  
  for i in range(3):
    deck.append("quantity 4\n" + make_card('Creature')[1:])
  for i in range(2):
    deck.append("quantity 4\n" + make_card('Sorcery')[1:])
  for i in range(2):
    deck.append("quantity 4\n" + make_card('Instant')[1:])
  for i in range(1):
    deck.append("quantity 2\n" + make_card('Artifact')[1:])
  for i in range(1):
    deck.append("quantity 2\n" + make_card('Enchantment')[1:])
  for i in range(1):
    deck.append("quantity 2\n" + make_card('Planeswalker')[1:])
  for i in range(4):
    deck.append("quantity 4\n" + make_card('Land')[1:])
  
  deck.append("quantity 4\n" + "name: Mana Confluence\nmana_cost: \ntype_line: Land\noracle_text: {T}, Pay 1 life: Add one mana of any color.\n")

  deck.append("quantity 4\n" + "name: City of Brass\nmana_cost: \ntype_line: Land\noracle_text: Whenever City of Brass becomes tapped, it deals 1 damage to you.\n{T}: Add one mana of any color.\n")

  deck.append("quantity 2\n" + "name: Gemstone Mine\nmana_cost: \ntype_line: Land\noracle_text: Gemstone Mine enters the battlefield with three mining counters on it.\n{T}, Remove a mining counter from Gemstone Mine: Add one mana of any color. If there are no mining counters on Gemstone Mine, sacrifice it.\n")

  return deck

def save_deck(deck: list) -> None:
  with open(f'Deck_{floor(time())}.txt', 'a') as file:
    for card in deck:      
      file.write(f'{card}\n')

def main():
  print(make_card('Creature'))

if __name__ == '__main__':
  main()


# save_deck(make_deck())
