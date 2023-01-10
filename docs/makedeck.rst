############
Making decks
############

``makedeck.py`` generates decklists based on a template. Requires trained model provided using ``--model`` flag. Templates specify how many cards of each type to make and how many copies of each card to include. A template can also specify some "static"/predetermined cards. The default template includes some preexisting rainbow lands for mana fixing.

=====
flags
=====

* ``--model``
* ``--deck_template``
* ``--output``
* ``--quantity``

-----------
``--model``
-----------

Default: None

Provide your model name so script knows where to send request. A typical model name looks like this: ``EXAMPLEMODEL:ft-personal-AN-EXAMPLE-TIMESTAMP``.

-------------------
``--deck_template``
-------------------

Default: ``config/deck_template_v1.json``

Specify a template and the script will try to make a conformant deck.

------------
``--output``
------------

Default: ``print``

Script can output to console or to file. Filename will be based on a timestamp like so: ``output/Deck_EXAMPLETIMESTAMP.txt``

^^^^^^^
options
^^^^^^^

* ``print``
* ``save``

--------------
``--quantity``
--------------

Default: ``1``

Generate N decks.