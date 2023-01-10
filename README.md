Momir is a set of tools for using AI models to generate Magic: The Gathering cards.

This works by fine-tuning a customized version of OpenAI's ChatGPT for card generation.

Eventually, it will also produce card images and configuration files to make the cards usable in Cockatrice.

---

### example:

```sh
python makecard.py --model "YOURMODELNAMEHERE" --supertype 'instant' --temperature 0.9
```
```
 name: What the?!
mana_cost: {2}{B}
type_line: Instant
oracle_text: Name a card. Target opponent reveals their hand, then discards all cards with the chosen name.
```

---

### docs:

[https://momir.readthedocs.io/en/latest/](https://momir.readthedocs.io/en/latest/)