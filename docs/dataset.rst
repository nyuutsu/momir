#############
Training data
#############

``dataset.py`` creates a dataset for training an ML model to generate cards. Downloads blob of all-card-data, curates by card name or legality, filters for relevand fields, arranges into completions.

Creates or overwrites ``output/trainingdata.jsonl``.

Defaults assume ``scrape.py`` has been run using defaults also, yielding ``output/cards_in_legacy_mainboard_all.jsonl`` for it to use as an input. Use flags to tell it the name of alternative whitelist file or to select a format legality-based whitelist.

=====
flags
=====

* ``--file_filter``
* ``--format_filter``
* ``--granularity``

-----------------
``--file_filter``
-----------------

Default: ``cards_in_legacy_mainboard_all.jsonl``

Default curation method; mutually exclusive with ``--format_filter``.

Default whitelist is "cards ever used in a winning legacy mainboard". File is a case-sensitive .jsonl of card names. Whitelisted cards are turned into prompts.

Intended for use with ``scrape.py`` outputs, but would work for a user-authored file. Use a card-name whitelist. 

^^^^^^^
options
^^^^^^^

``relative/path/to/file.jsonl`` e.g. ``output/cards_in_legacy_mainboard_last_two_weeks.jsonl``

-------------------
``--format_filter``
-------------------

Default: None

Alternate curation method; mutually exclusive with ``--file_filter``.

Default whitelist is "cards legal in legacy". Whitelisted cards are turned into prompts.

The ``oldschool`` option would probably make for a cool model. *If you can figure out how to extract the alpha rules text as printed, let me know!*

^^^^^^^
options
^^^^^^^

============= ========= =========== ======== =====
Singleton     Eternal   Nonrotating Rotating Retro
============= ========= =========== ======== =====
commander     vintage   modern      standard oldschool
brawl         legacy    pioneer     future   premodern
historicbrawl pauper    explorer    alchemy
duel          commander historic    penny
gladiator          
============= ========= =========== ======== =====

-----------------
``--granularity``
-----------------

Default: ``low``

Training data can be "just supertype" or "supertype, color and cmc". The latter *works* but later pipeline stages haven't been tested yet.

^^^^^^^
options
^^^^^^^

* ``low``: training data prompts will be general, like this: ``{"prompt":"Instant ->","completion":" name: Brainstorm\nmana_cost: {U}\ntype_line: Instant\noracle_text: Draw three cards, then put two cards from your hand on top of your library in any order.\nꙮ"}``
* ``high``: training data prompts will be specific, like this: ``{"prompt":"CMC 1 ['U'] Instant ->","completion":" name: Brainstorm\nmana_cost: {U}\ntype_line: Instant\noracle_text: Draw three cards, then put two cards from your hand on top of your library in any order.\nꙮ"}``