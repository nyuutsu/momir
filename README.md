tools for ai-generated mtg card tasks

eventually, a workflow for generating cockatrice-playable ai-generated decks

`scrape.py` prepares an optional filter to be used by `dataset.py`

it scrapes mtgtop8's "top cards [in format]" page for a list of all cards that have been used in a format and timespan

by default it looks for "all cards ever used in legacy". this can be modified with flags. example use:

`chmod +x scrape.py`

`./scrape.py --timeframe 'last_two_weeks'`

`./scrape.py --help` gives some information on this. more can be found by looking at the valid date periods for each format in `format_mappings.json`. there are a lot of them and many of them are exclusive to one format.

`dataset.py` prepares training data:

1. download all card data from scryfall

2. use filter rules to exclude portions of the cardpool

~~the default filter, `filters.json`, should filter for "vintage-legal single-faced card"~~ deprecated

the default filter should find everything in legacy and exclude everything else. to override this with a different format: `--format_filter FORMAT`

it is also possible to use a result from `scrape.py` as the filter. to do this, use flag `--file_filter FILENAME`.

handling for + inclusion of double-faced cards to be added later

3. use pruning rules in `unneeded attributes.json` to remove data not needed for completions

4. write result to `training_data.jsonl` formatted as prompts to create a card of a given main type

example use:

`chmod +x dataset.py`

`python dataset.py --file_filter "cards_in_legacy_mainboard_all.jsonl"`

this will create `training_data.jsonl`. its intended use is to feed to openai for fine-tuning one of their models w/ could be done like so:

```openai api fine_tunes.create -t training_data.jsonl -m davinci --n_epochs 1```

*if the above command doesn't work: check oa package installed + python in path + api key in path + you in right cwd*

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

`pictures.py`

experiment re: drawing text on card frames. eventally will be part of a tool for automating making cockatrice-playable versions of generated cards
