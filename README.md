## tools for ai-generated mtg card tasks

(eventually, a workflow for generating cockatrice-playable ai-generated decks)

### tl;dr instructions:

0. run `pip install -r requirements.txt`

1. run `python scrape.py`
  should scrape data and store in `/output`

2. run `python dataset.py`
  should process data to create a training dataset and store as `/output/trainingdata.jsonl`

3. run `openai api fine_tunes.create -t output/training_data.jsonl -m davinci --n_epochs 1`
  when this works it will output a "model name"; copy this.

4. run `python maker.py --model "YOURMODELNAMEHERE" --supertype "creature"`
  should generate a creature and print it
  *most of the features aren't done. it will make single cards though!*

~~5. something involving pictures.py~~ ***coming soon***

---
### elaboration

#### `scrape.py`

`scrape.py` prepares an optional filter to be used by `dataset.py`

It scrapes mtgtop8's "top cards [in format]" page for a list of all cards that have been used in a format and timespan. By default it looks for "all used in legacy over past two weeks". This behavior can be modified with flags.

It creates a .jsonl file in `output`; name will vary based on options used. The default options result in a file named `cards_in_legacy_mainboard_last_two_weeks.jsonl`

flags: `--deck`, `--format`, `--timeframe`

##### `--deck`:
Default: `main`
Site has separate lists/search results for "mainboard" vs "sideboard"
Script default behavior is to scrape mainboard
If want *both*: for now must run twice and maybe combine results from there
This will be improved in a later version.

###### *options*

* `main` maindeck results
* `side` sideboard results

##### `--format`:
Default: `legacy`
Site has data on several formats. you can pick which one to scrape from. Each format has a different slate of supported timeframes.

###### *options*
* `legacy`
* `vintage`
* `modern`
* `pauper`
  
##### `--timeframe`:
Default: `all`
Formats have different available timeframes. `timeframe`, if given, must be compatible with the `format`. Compatability listed below:

###### *options*

| legacy | vintage |  modern | pauper
| - | - | - | - 
| last_two_weeks | last_two_months | last_two_weeks | last_two_months |
| last_two_months | last_four_months | last_two_months | last_four_months |
| last_two_months | live_last_six_months | major_last_two_months | live_last_three_months |
| last_two_weeks | all_2022 | live_last_two_months | all_2022 |
| major_last_four_months | all_2020-2021 | all_2022 | all_2021 |
| live_last_two_months | all_2018-2019 | all_2021 | all_2020 |
| all_2022 | all_2015-2017 | all_2020 | all_2019 |
| all_2021 | all_2011-2014 | all_2019 | all_2018 |
| all_2020 | all_major | all_2018 | all_2017 |
| all_2019 | all | all_2017 | all_2016 |
| all_2018 |  | all_2016 | all |
| all_2017 |  | all_2015 |  |
| all_2016 |  | all_2014 |  |
| all_2015 |  | all_2013 |  |
| all_2014 |  | all_2012 |  |
| all_2013 |  | all_2011 |  |
| all_2012 |  | all |  |
| all_2011 |  | all_pt_and_gp |  |
| all_major |  |  |  |
| all |  |  |  |
---
#### `dataset.py`

`dataset.py` prepares a training dataset to be used for training an ML model to create cards based on that dataset. It begins by downloading a blob of "all data about all cards" and then curating out unwanted parts.

By default, it assumes you ran `scrape.py` with no flags and so have created `output/cards_in_legacy_mainboard_all.jsonl` for it to use as an input.
If you have not or won't do this, read on for other options. It creates or overwrites the file `trainingdata.jsonl` in `output`.

flags: `--file_filter`, `--format_filter`, `--granularity`

##### `--file_filter`:
Default: `cards_in_legacy_mainboard_all.jsonl`
Dataset curation method is to use a card-name whitelist. The default whitelist is "cards ever used in a winning legacy mainboard". Whitelist file should be a newline-separated, case-sensitive list of card names. Cards on whitelist are converted into prompts; cards not on list are excluded. Intended for use with `scrape.py` outputs, but would work for a user-authored file.

###### *options*:

`relative/path/to/file.jsonl` e.g. `output/cards_in_legacy_mainboard_last_two_weeks.jsonl`

##### `--format_filter`:
Default: none
Overrides dataset curation method to instead include based on legality in a format. Cards in format are converted into prompts; cards not in format are excluded. Will in most cases result in *very large* training sets. The `oldschool` option would probably make for a cool model.

###### *options*

| Eternal | Singleton | Nonrotating | Rotating | Retro |
| - | - | - | - | - 
| vintage | commander | modern | standard | oldschool |
| legacy | brawl | pioneer | future | premodern |
| pauper | historicbrawl | explorer | alchemy
| commander | duel | historic | penny
|  | gladiator |

##### `--granularity`:
Default: `low`
Making a card consists of giving the trained model a "prompt" and getting a result. A wide prompt will have more variety per prompt and be slightly easier to use. A narrow prompt will probably be more useful for autogenerating decklists. The dataset can be of wide or narrow prompts. Wide prompts are just a card's main supertype. Narrow prompts are also a color and a converted mana cost. Both modes should be compatible with using `--file_filter` or `--format_filter`.

###### *options*

* `low`: training data prompts will be wide, like this: `{"prompt":"Instant ->","completion":" name: Brainstorm\nmana_cost: {U}\ntype_line: Instant\noracle_text: Draw three cards, then put two cards from your hand on top of your library in any order.\nꙮ"}`
* `high`: training data prompts will be narrow, like this: `{"prompt":"CMC 1 ['U'] Instant ->","completion":" name: Brainstorm\nmana_cost: {U}\ntype_line: Instant\noracle_text: Draw three cards, then put two cards from your hand on top of your library in any order.\nꙮ"}`
---
#### `maker.py`

`maker.py` generates magic cards. It needs you to have already trained a model using a dataset (such as one produced by `dataset.py`). Its default behavior is "generate one creature and print it to the console". Soon, this behavior can be modified with flags.

flags: `--tbd`, `--alsotbd`

##### `--flag`:
Default: tbd
tbd

###### *options*:
* `tbd`
---
#### `pictures.py`

`pictures.py` is incomplete. Don't use this for now.

flags: `--tbd`, `--alsotbd`

##### `--tbd`:
tbd

###### *options*:
* `tbd`
---

### Troubleshooting:

Check that:
* required packages are installed
* python is in PATH
* openai API key is in PATH
* openai account has funding
* you are in the right directory (`momir/`)

It's entirely possible that I've missed something. Bug/error reports enthusiastically welcome.