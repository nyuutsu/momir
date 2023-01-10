Momir is a set of tools for using AI models to generate Magic: The Gathering cards.

This works by fine-tuning a customized version of OpenAI's ChatGPT for card generation.

Eventually, it will also produce card images and configuration files to make the cards usable in Cockatrice.

### examples:

```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'creature' --temperature 0.9
```
```
 name: Amoeboid Phytohydra
mana_cost: {W}{U}
type_line: Creature — Plant Hydra
oracle_text: Morph—Reveal a green card in your hand, then discard a green card. (You may cast this card face down as a 2/2 creature for {3}. Turn it face up any time for its morph cost.)
When Amoeboid Phytohydra is turned face up, put a +1/+1 counter on each green creature you control.
Power of Phytohydra 1 (Whenever you cast a spell, you may put a +1/+1 counter on Phytohydra.)
color_indicator:1
power: 1
toughness: 2
```
⬆ this is great
```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'sorcery' --temperature 0.9
```
```
 name: Land Aid 'R' Us
mana_cost: {G}
type_line: Sorcery
oracle_text: Search your library for a land card, put it onto the battlefield, then shuffle.
enters_the_battlefield_tapped: Land
type: sorcery
```
⬆ name is delightful. way too strong.
```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'instant'
```
```
 name: Scornful Stroke
mana_cost: {U}{U}
type_line: Instant
oracle_text: Counter target spell you don't control.
Cycling {U}{U} ({U}{U}, Discard this card: Draw a card.)
When you cycle Scornful Stroke, counter target spell you don't control.
```
⬆ this is the greatest counterspell of all time. way too strong.
```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'instant' --temperature 0.9
```
```
 name: What the?!
mana_cost: {2}{B}
type_line: Instant
oracle_text: Name a card. Target opponent reveals their hand, then discards all cards with the chosen name.
```
⬆ this seems pretty reasonable to me

```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'creature' 
```
```
 name: Soul of Shauku, Endbringer
mana_cost: {X}{X}
type_line: Creature — Dragon Skeleton
oracle_text: Flying
When Soul of Shauku, Endbringer enters the battlefield, you determine the target of its ability. You may choose yourself or an opponent, or target any creature or planeswalker. If a planeswalker enters the battlefield under that planeswalker's controller's control in this way and wasn't already on the battlefield, it's considered a new planeswalker and had no power, toughness, or loyalty: put it into its owner's graveyard. If you don't, exile target creature.
power: 0
toughness: 0
```
⬆ sometimes the output is sort of bad. sometimes a bad output is funny. this is a lot of words for what amounts to "0: exile target creature" 😂

---

### basic idea:

1. AI-generated cards might benefit from being trained on only an interesting subset of the cardpool rather than on the whole thing.

2. Running the scripts in order described below prepares training data of an "interesting subset". By default: stuff ever used in a winning legacy maindeck. This is done by getting a list of all-card-and-all-card-data, scraping a whitelist of card names, using that whitelist to exclude the irrelevant majority of the cardpool, and conforming the relevant part of the remaining info into completions.

  * There are also flags available for scraping different and/or smaller segments of the cardpool, or for instead using simple format legality as the filter.

4. This can be used to fine-tune a model and have it make cards for you.

### tl;dr instructions:

0. preliminary:
    
    i. install dependencies / requirements

      * run `pip install -r requirements.txt`

      * install firefox

    ii. make an [openai account](https://openai.com/api/pricing/), create an api key, and store the key in your PATH as OPENAI_API_KEY.
    
    how to store the key:
    * windows, powershell (maybe cmd works too?):
      * run `setx OPENAI_API_KEY "YOURKEYHERE"`
      * close + reopen window
    * unixlike: 
      * run `echo "export OPENAI_API_KEY='YOURKEYHERE'" >> ~/.zshrc`
        * (or `… >> ~/.bashrc` or similar if applicable)
      * run `source ~/.zshrc`
        * (or `… >> ~/.bashrc` or similar if applicable)

1. run `python scrape.py`

    if mtgtop8 is cooperative, this will scrape its data and store in `/output`

2. run `python dataset.py`

    will process scrape data to create a training dataset and store as `/output/trainingdata.jsonl`

3. run `openai api fine_tunes.create -t output/training_data.jsonl -m davinci --n_epochs 1 --learning_rate_multiplier 0.02`

    this will output a "model name"; copy this & paste it into "YOURMODELNAMEHERE" in the `make….py` command in the next step.

4. run a `make….py` command:
  
    * `python makecard.py --model "YOURMODELNAMEHERE" --quantity 10`
  generate 10 creatures and print them

    * `python makedeck.py --model "YOURMODELNAMEHERE" --output "save"`
  generate one 60-card deck and and save it to `output/Deck_TIMESTAMP.txt`

    * ~~`python makeset.py --model "YOURMODELHERE"`
  generate one 350-card set and save it to `output/Set_TIMESTAMP.txt`~~ ***coming soon***

5. ~~pictures.py card image generation~~ ***coming soon***

6. ~~cockatrice.py cockatrice data generation~~ ***coming soon***

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

Default: None

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

flags: `--model`, `--supertype`, `--temperature`, `--filename`, `--quantity`

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

##### `--temperature`:

Default: `1`

Enter a temperature value to modify how 'surprising' the outputs are. Current implenetation asks model for a result and then throws it out and retries if there is a name collision with an official card. Lowering the temperature too much will increase the rate of collisions such that it will take a very long time to get outputs. Probably don't set this lower than about 0.9.

##### `--filename`:

Default: None

Script can output to console or to file. If a filename is offered that file will be created or appended to in `/output`. If not, results printed to console.

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

#### ~~`makeset.py`~~ ***coming soon***

`makeset.py` is in the earliest stages of trying stuff out. Don't use this yet.

What this is *going* to do is generate card sets using a template. A template specifies how many cards of each type to make.

It will be possible to use a 'high granularity' model with a 'high granularity' template to make very specific set compositions.

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

#### ~~`pictures.py`~~ ***coming soon***

`pictures.py` is in the earliest stages of just trying stuff out. Don't use this yet.

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
* you are in the right directory (`momir/`)
* firefox installed
* mtgtop8 isn't rate-limiting you into oblivion
* openai API key is in PATH
* openai account has funding
  * at time of writing, new openai accounts get $12 of credits & the default output of scrape.py costs ~$8.50 to train

Bug/error reports enthusiastically welcome.