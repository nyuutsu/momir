tools for ai-generated mtg card tasks

`dataset.py` prepares training data:

1. download all card data from scryfall

2. use filter rules to exclude portions of the cardpool

the default filter, `filters.json`, should filter for "vintage-legal single-faced card"

handling for + inclusion of double-faced cards to be added later

more options for this filtering will be added. main ones of interest to me are "legacy legal", "legacy playable"

3. use pruning rules in `unneeded attributes.json` to remove data not needed for completions

4. write result to `training_data.jsonl` formatted as prompts to create a card of a given main type

intended use is to feed to openai for fine-tuning one of their models w/ could be done like so:

```openai api fine_tunes.create -t training_data.jsonl -m davinci --n_epochs 1```

*if the above command doesn't work: check oa package installed + python in path + you in right cwd*

running the above command should return a model name. default names currently look something like this:

`davinci:ft-personal-2022-12-27-16-04-13`

*this model game is used in the "model" field in the api call in `maker.py`'s `make_card()`*

`maker.py`

makes cards using the model

right now has two uses:

1. make a single card of a given [main] [super] type

  e.g. make_card('Creature') -> returns `name: Ryans Remembrance\nmana_cost: {2}\n`...[etc]

2. make a decklist of 60 cards, of which most or all are ai-generated

  this writes the result to disk in a file w/ quantities

  right now, deckbuilder traits are hardcoded. e.g. all decks have creaturebase of "playsets of three creatures", all decks have some rainbowlands for fixing, etc. this will be improved to allow prompting for a specific color combination, curve, and type breakdown

`pictures.py'

experiment re: drawing text on card frames. eventally will be part of a tool for automating making cockatrice-playable versions of generated cards