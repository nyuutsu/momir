import argparse
import json
import logging
from os import makedirs
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

def scrape_format(args):
  logging.info('beginning scrape_format()')
  cards = ""
  page_counter = 1
  driver = webdriver.Firefox(service_log_path=join('logs', 'geckodriver.log'))
  driver.implicitly_wait(10)

  with open(join('config', 'format_abbreviations.json')) as file:
    abbreviations = json.load(file)
  abbreviation = abbreviations[args.format]

  with open(join('config', 'format_mappings.json')) as file:
    mappings = json.load(file)
  mapping = mappings[args.format][args.timeframe]

  url = f'https://www.mtgtop8.com/topcards?f={abbreviation}&meta={mapping}'
  logging.info('url preparation seems ok: {url}')
  driver.get(url)

  if args.deck == 'side':
    logging.info('attempting to access side deck results')
    main_sideboard_toggles = driver.find_elements(by=By.NAME, value="maindeck")
    main_sideboard_toggles[1].click()
    submit_form = driver.find_elements(by=By.TAG_NAME, value="input")
    submit_form[4].click()
  
  while driver.find_elements(by=By.CLASS_NAME, value="L14"):
    logging.info(f'🮐🮐🮐🮐🮐 Page {page_counter} Start 🮐🮐🮐🮐🮐')  
    results = driver.find_elements(by=By.CLASS_NAME, value="L14")
    for k, v in enumerate(results):
      if k % 3 == 0:
        cards += f'{v.text}\n'
        logging.info(v.text)

    logging.info(f'🮐🮐🮐🮐🮐 Page {page_counter} End 🮐🮐🮐🮐🮐')
    page_counter = page_counter + 1
    driver.execute_script(f'PageSubmit({page_counter})')

    WebDriverWait(driver, timeout=10).until(staleness_of(results[0]))

  logging.info('looks like reached end of results')
  driver.quit()
  return cards

def log_to_file(data, args):
  makedirs('./output', exist_ok=True)
  with open(join('output', f'cards_in_{args.format}_{args.deck}board_{args.timeframe}.jsonl'), 'w') as file:
    file.write(data)

def parse_args():
  parser = argparse.ArgumentParser(description="a script to scrape mtgtop8 'cards used in a format'")

  parser.add_argument("--format", type=str, default="legacy", choices=['vintage', 'legacy', 'modern', 'pauper'])

  # site doesn't allow 'both'
  parser.add_argument("--deck", type=str, default="main", choices=['main', 'side'])
  parser.add_argument("--timeframe", type=str, default="all",
                      help="default is 'last_two_weeks'; see readme for more options")
  args = parser.parse_args()
  with open(join('config', 'format_mappings.json')) as file:
    test = json.load(file)
  try:
    test[args.format][args.timeframe]
  except KeyError:
    logging.critical('invalid timeframe for format; see readme.md for format-specific options')
    exit()
  logging.info('arguments seem parsed')
  return args

def main():
  makedirs('./logs', exist_ok=True)
  logging.basicConfig(filename=join('logs', 'scrape.log'), encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()
  scrape_result = scrape_format(arguments)
  log_to_file(scrape_result, arguments)


if __name__ == '__main__':
  main()
