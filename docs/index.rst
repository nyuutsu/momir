===================
Momir documentation
===================

Momir is a set of tools for using AI models to generate Magic: The Gathering cards. This works by fine-tuning a customized version of OpenAI's ChatGPT for card generation. Eventually, it will also produce card images and configuration files to make the cards usable in Cockatrice.

-----------
Example use
-----------

>>> python makecard.py --model "YOURMODELNAMEHERE" --supertype 'creature' --temperature 0.9
name: Amoeboid Phytohydra
mana_cost: {W}{U}
type_line: Creature — Plant Hydra
oracle_text: Morph—Reveal a green card in your hand, then discard a green card. (You may cast this card face down as a 2/2 creature for {3}. Turn it face up any time for its morph cost.)
When Amoeboid Phytohydra is turned face up, put a +1/+1 counter on each green creature you control.
Power of Phytohydra 1 (Whenever you cast a spell, you may put a +1/+1 counter on Phytohydra.)
color_indicator:1
power: 1
toughness: 2

⬆ This is great.

>>> python makecard.py --model "YOURMODELNAMEHERE" --supertype 'sorcery' --temperature 0.9
name: Land Aid 'R' Us
mana_cost: {G}
type_line: Sorcery
oracle_text: Search your library for a land card, put it onto the battlefield, then shuffle.
enters_the_battlefield_tapped: Land
type: sorcery

⬆ Name is delightful. Way too strong.

>>> python makecard.py --model "YOURMODELNAMEHERE" --supertype 'instant'
name: Scornful Stroke
mana_cost: {U}{U}
type_line: Instant
oracle_text: Counter target spell you don't control.
Cycling {U}{U} ({U}{U}, Discard this card: Draw a card.)
When you cycle Scornful Stroke, counter target spell you don't control.

⬆ This is the greatest counterspell of all time. Way too strong.

>>> python makecard.py --model "YOURMODELNAMEHERE" --supertype 'instant' --temperature 0.9
name: What the?!
mana_cost: {2}{B}
type_line: Instant
oracle_text: Name a card. Target opponent reveals their hand, then discards all cards with the chosen name.

⬆ This seems pretty reasonable to me!

>>> python makecard.py --model "YOURMODELNAMEHERE" --supertype 'creature' 
name: Soul of Shauku, Endbringer
mana_cost: {X}{X}
type_line: Creature — Dragon Skeleton
oracle_text: Flying
When Soul of Shauku, Endbringer enters the battlefield, you determine the target of its ability. You may choose yourself or an opponent, or target any creature or planeswalker. If a planeswalker enters the battlefield under that planeswalker's controller's control in this way and wasn't already on the battlefield, it's considered a new planeswalker and had no power, toughness, or loyalty: put it into its owner's graveyard. If you don't, exile target creature.
power: 0
toughness: 0

⬆ Sometimes the output is bad but funny. This is a lot of words for what amounts to "0: exile target creature". 😂

.. note::

   This project is under active development.

--------
Contents
--------

.. toctree::

  index
  glance
  pipeline
  trouble
