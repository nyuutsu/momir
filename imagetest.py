from PIL import Image, ImageFont, ImageDraw
from textwrap import fill

def generate_card_art(card: str):
  print(card.split('\n'))
  name, cost, type, oracle, stats, morestats = [n.split(':')[1] for n in card.split('\n')]
  
  template = Image.open("pics/blank.png")
  art = Image.open("pics/creature.png").resize((600, 600))
  image_editable = ImageDraw.Draw(template)

  mask = Image.new("L", art.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((0, 0, 578, 470), fill=255)

  template.paste(art, (83, 98), mask)
  
  wrapped_text = fill(name, 20)
  title_font = ImageFont.truetype('fira_mono.otf', 50)
  image_editable.text((20,30), wrapped_text, (0, 0, 0), font=title_font)

  wrapped_text = fill(cost, 20)
  title_font = ImageFont.truetype('fira_mono.otf', 50)
  image_editable.text((450,30), wrapped_text, (0, 0, 0), font=title_font)

  wrapped_text = fill(type, 35)
  type_font = ImageFont.truetype('fira_mono.otf', 40)
  image_editable.text((30,570), wrapped_text, (0, 0, 0), font=type_font)

  wrapped_text = fill(oracle, 35)
  oracle_font = ImageFont.truetype('fira_mono.otf', 25)
  image_editable.text((100,625), wrapped_text, (0, 0, 0), font=oracle_font)

  """
  observation:
  card[0] is always name, card[1] is cost etc
  card[-1] will USUALLY be "stats". maybe loyalty maybe toughness
  depending on what -1 is the oracle text is going to be like card[5:-2] or card[5:-3] but it's so fiddly
  this approach probably dead end
  """

  wrapped_text = fill(f'{stats}/{morestats.strip()}', 35)
  type_font = ImageFont.truetype('fira_mono.otf', 50)
  image_editable.text((575, 925), wrapped_text, (0, 0, 0), font=type_font)

  template.save("outputs/result.png")

def main():
  test_card = """name: Demonslayer
mana_cost: {1}{W}
type_line: Creature — Human Cleric
oracle_text: When Demonslayer enters the battlefield, destroy target Demon.
power: 2
toughness: 3"""
  generate_card_art(test_card)
  
if __name__ == '__main__':
  main()