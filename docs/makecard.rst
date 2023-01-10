############
Making cards
############

``makecard.py`` generates individual cards. Requires trained model provided using ``--model`` flag. Default is "generate one creature. if name collision with a real card, try again. if name is new, print card to the console".

A properly structured request looks like this: ``python makecard.py --model "PASTEYOURMODELNAMEHERE"``

=====
flags
=====

* ``--model``
* ``--supertype``
* ``--temperature``
* ``--filename``
* ``--quantity``

-----------
``--model``
-----------

Default: None

Provide your model name so script knows where to send request. A typical model name looks like this: ``EXAMPLEMODEL:ft-personal-AN-EXAMPLE-TIMESTAMP``.

---------------
``--supertype``
---------------

Default: ``Creature``

Provide a main supertype and the model will *try* to make something of that type. Occasionally it might make something of the wrong type. Type validation will be added eventually. Possible types will vary based on training data.

^^^^^^^^^
*options*
^^^^^^^^^

Most training sets will allow these:

* ``Creature``
* ``Sorcery``
* ``Instant``
* ``Artifact``
* ``Enchantment``
* ``Land``

Many training sets will allow these:
  
* ``Planeswalker``
* ``Tribal``

Hypothetically possible:

* ``Conspiracy``
* ``Dungeon``
* ``Plane``
* ``Phenomenon``
* ``Scheme``
* ``Vanguard``

-----------------
``--temperature``
-----------------

Default: ``1``

Enter a temperature to change how 'surprising' the cards are. Lower values should be more 'sensible' but will take longer due to more name collisions. Probably don't set this lower than about 0.9 unless you are *very* patient and willing to spend a lot of openai credits per card.


--------------
``--filename``
--------------

Default: None

If given, file will be appended to in ``/output``. Else results printed to console.

--------------
``--quantity``
--------------

Default: ``1``

Generate N cards.