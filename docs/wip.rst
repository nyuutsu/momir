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
Unexpected indentation.
* `print`
* `save`

##### `--quantity`:
Unexpected indentation.
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