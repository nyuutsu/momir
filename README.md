## tools for ai-generated mtg card tasks

(eventually, a workflow for generating cockatrice-playable ai-generated decks)

### tl;dr instructions:

0. run `pip install -r requirements.txt`

    * make an [openai account](https://openai.com/api/pricing/) and get an api key
    * store the key in your PATH
      * windows, cmd/powershell:
        * run `setx OPENAI_API_KEY "YOURKEYHERE"`
        * close + reopen window
      * unixlike: 
        * run `echo "export OPENAI_API_KEY='YOURKEYHERE'" >> ~/.zshrc`
          * (or `… >> ~/.bashrc` or similar if applicable)
        * run `source ~/.zshrc`
          * (or `… >> ~/.bashrc` or similar if applicable)

1. run `python scrape.py`
  should scrape data and store in `/output`

1. run `python dataset.py`
  should process data to create a training dataset and store as `/output/trainingdata.jsonl`

1. run `openai api fine_tunes.create -t output/training_data.jsonl -m davinci --n_epochs 1 --learning_rate_multiplier 0.02`
  when this works it will output a "model name"; copy this.

1. run a `make….py` command:
  
    * `python makecard.py --model "YOURMODELNAMEHERE" --quantity 10`
  generate 10 creatures and print them

    * `python makedeck.py --model "YOURMODELNAMEHERE" --output "save"`
  generate one 60-card deck and and save it to `output/Deck_TIMESTAMP.txt`

    * ~~`python makeset.py --model "YOURMODELHERE"`
  generate one 350-card set and save it to `output/Set_TIMESTAMP.txt`~~ ***coming soon***

~~5. pictures.py card image generation~~ ***coming soon***

~~6. cockatrice.py cockatrice data generation~~ ***coming soon***

---
### elaboration

#### `scrape.py`

`scrape.py` prepares an (optional w/ flags; required w/o flags) filter to be used by `dataset.py`

It scrapes mtgtop8's "top cards [in format]" page for a list of all cards that have been used in a format and timespan. By default it looks for "all cards ever used in legacy mainboards". This behavior can be modified with flags.

It creates a .jsonl file in `output`; name will vary based on options used. The default options result in a file named `cards_in_legacy_mainboard_all.jsonl`

flags: `--deck`, `--format`, `--timeframe`, `--headless`

##### `--deck`:

Default: `main`

Site has separate lists/search results for "mainboard" vs "sideboard". Script default behavior is to scrape mainboard. If want *both*: for now must run twice and maybe combine results from there. This will be improved in a later version.

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

##### `--headless`:

Default: `false`

The scraper launches an automated browser it uses to interact with the website. By default, this browser is drawn onscreen so you can monitor it.

###### *options*

* `false` visible scraper window
* `true` invisible scraper window
  
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

#### `makecard.py`

`maker.py` generates individual magic cards. It needs you to have already trained a model using a dataset (such as one produced by `dataset.py`) & to provide the model's name using the `--model` flag. Its default behavior is "generate one creature and print it to the console". This behavior can be modified with flags.

A properly structured request looks something like this: `python makecard.py --model "PASTEYOURMODELNAMEHERE"`

flags: `--model`, `--supertype`, `--output`, `--quantity`

##### `--model`:

Default: None

Must provide model name so script knows where to send the request. A model name looks something like this: `EXAMPLEMODEL:ft-personal-AN-EXAMPLE-TIMESTAMP`.

##### `--supertype`:

Default: `Creature`

Specify a main supertype and the model will try to make something of that type. Available types will vary based on training data used.

###### *options*:

Most training sets will allow these:

* `Creature`
* `Sorcery`
* `Instant`
* `Artifact`
* `Enchantment`
* `Land`

Many training sets will allow these:
  
* `Planeswalker`
* `Tribal`

Hypothetically possible:

* `Conspiracy`
* `Dungeon`
* `Plane`
* `Phenomenon`
* `Scheme`
* `Vanguard`

##### `--output`:

Default: `print`

Script can output to console or to file. Filename will be based on a timestamp like so: `output/Cards_TIMESTAMPGOESHERE.txt`

###### *options*:

* `print`
* `save`

##### `--quantity`:

Default: `1`

Enter a number to generate that many cards

#### `makedeck.py`

`makedeck.py` uses a template to generate decklists. A template specifies how many cards of each type to make and how many copies of each card to include. A template can also specify some "static"/predetermined cards. The default template includes some preexisting rainbow lands for mana fixing.

flags: `--model`, `--deck_template`, `--output`, `--quantity`

##### `--model`:

Default: None

Must provide model name so script knows where to send the request. A model name looks something like this: `EXAMPLEMODEL:ft-personal-AN-EXAMPLE-TIMESTAMP`.

##### `--deck_template`:

Default: `config/deck_template_v1.json`

Specify a template and the script will try to make a conformant deck.

##### `--output`:

Default: `print`

Script can output to console or to file. Filename will be based on a timestamp like so: `output/Deck_EXAMPLETIMESTAMP.txt`

###### *options*:

* `print`
* `save`

##### `--quantity`:

Default: `1`

Enter a number to generate that many decks

#### `makeset.py`

`makeset.py` uses a template to generate card sets. A template specifies how many cards of each type to make. The default template specifies 350 cards of various types.

In the future it will be possible to use a 'high granularity' model with a 'high granularity' template to make very specific set compositions. This might get its own flag.

flags: `--model`, `--set_template`, `--output`, `--quantity`

##### `--model`:

Default: None

Must provide model name so script knows where to send the request. A model name looks something like this: `EXAMPLEMODEL:ft-personal-AN-EXAMPLE-TIMESTAMP`.

##### `--set_template`:

Default: `config/set.json`

Specify a template and the script will try to make a conformant set.

##### `--output`:

Default: `print`

Script can output to console or to file. Filename will be based on a timestamp like so: `output/Set_EXAMPLETIMESTAMP.txt`

###### *options*:

* `print`
* `save`

##### `--quantity`:

Default: `1`

Enter a number to generate that many sets

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