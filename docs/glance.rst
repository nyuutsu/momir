=================
Momir at a glance
=================

----
What
----

0. These scripts prepare training data of subsets of the Magic cardpool, which can be used to fine-tune a model.

  * The default behavior is to prepare "everything ever used in a winning legacy maindeck", but there are other options.

1. These scripts also provide a few mechanisms for using the model to generate cards.

2. Eventually these scripts will also auotomate producing cockatrice data for those cards.

---
Why
---

0. AI-generated versions of things can be cool. Magic is cool.

1. AI-generated cards might benefit from being trained on interesting subsets of the cardpool rather than on the whole thing.

---
How
---

0. preliminary:
    
  1. install dependencies / requirements

    * run ``pip install -r requirements.txt``

    * install firefox

  2. make an `openai account <https://openai.com/api/pricing/>`_, create an api key, and store the key in your PATH as OPENAI_API_KEY.
  
    how to store the key:

      * windows, powershell (maybe cmd works too?):

        1. run ``setx OPENAI_API_KEY "YOURKEYHERE"``

        2. close + reopen window

      * unixlike: 

        1. run ``echo "export OPENAI_API_KEY='YOURKEYHERE'" >> ~/.zshrc``

          * (or ``… >> ~/.bashrc`` or similar if applicable)

        2. run ``source ~/.zshrc``

          * (or ``… >> ~/.bashrc`` or similar if applicable)

1. run ``python scrape.py``

  if mtgtop8 is cooperative, this will scrape its data and store in ``/output``

2. run ``python dataset.py``

  will process scrape data to create a training dataset and store as ``/output/trainingdata.jsonl``

3. run ``openai api fine_tunes.create -t output/training_data.jsonl -m davinci --n_epochs 1 --learning_rate_multiplier 0.02``

  will output a "model name"; copy this & paste it into "YOURMODELNAMEHERE" in a ``make….py`` command in the next step.

4. run a ``make….py`` command:
  
  * generate 10 creatures and print them:
  
    * ``python makecard.py --model "YOURMODELNAMEHERE" --quantity 10``
  
  * generate one 60-card deck and and save it to ``output/Deck_TIMESTAMP.txt``:

    * ``python makedeck.py --model "YOURMODELNAMEHERE" --output "save"``
  
*coming soon*:

0. generate card set based on template

1. generate card images

2. generate cockatrice data