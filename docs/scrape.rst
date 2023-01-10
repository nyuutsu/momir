########
Scraping
########

``scrape.py`` creates a filter to be used by ``dataset.py``

Scrapes mtgtop8's "top cards in [format] over [timeframe] in [main/sideboard]" page for all cards used format + timespan + boardtype.

Creates .jsonl file in ``output``; named based on options used. Default options yield file named ``cards_in_legacy_mainboard_all.jsonl``

=====
flags 
=====

* ``--deck``
* ``--format``
* ``--timeframe``
* ``--headless``

----------
``--deck``
----------
  
Default: ``main``

Scrape "mainboard" or "sideboard" results. Site we're scraping lists these separately. Later version will allow "both".

^^^^^^^
options
^^^^^^^

* ``main`` maindeck results
* ``side`` sideboard results

------------
``--format``
------------

Default: ``legacy``

Site has data for several formats. Can pick a ``--format`` in conjunction with a ``--timeframe``. Each format has a different slate of supported timeframes, compatibility documented in ``--timeframe``

^^^^^^^
options
^^^^^^^

* ``legacy``
* ``vintage``
* ``modern``
* ``pauper``
  
---------------
``--timeframe``
---------------

Default: ``all``

Formats have different supported timeframes. ``--timeframe`` must be compatible with the ``format``. Compatability is listed below.

^^^^^^^
options
^^^^^^^

====================== ==================== ===================== ================
       legacy               vintage                 modern            pauper
====================== ==================== ===================== ================
last_two_weeks         last_two_months      last_two_weeks        last_two_months
last_two_months        last_four_months     last_two_months       last_four_months
last_two_months        last_four_months     last_two_months       last_four_months
last_two_months        live_last_six_months major_last_two_months live_last_three_months
last_two_weeks         all_2022             live_last_two_months  all_2022
major_last_four_months all_2020-2021        all_2022              all_2021
live_last_two_months   all_2018-2019        all_2021              all_2020
all_2022               all_2015-2017        all_2020              all_2019
all_2021               all_2011-2014        all_2019              all_2018
all_2020               all_major            all_2018              all_2017
all_2019               all                  all_2017              all_2016
all_2018                                    all_2016              all
all_2017                                    all_2015
all_2016                                    all_2014
all_2015                                    all_2013
all_2014                                    all_2012
all_2013                                    all_2011
all_2012                                    all
all_2011                                    all_pt_and_gp
all_major                              
all
====================== ==================== ===================== ================

--------------
``--headless``
--------------

Default: ``false``

Scraper launches an automated browser to interact with site. Visible by default.

^^^^^^^
options
^^^^^^^

* ``false`` visible scraper window
* ``true`` invisible scraper window
  