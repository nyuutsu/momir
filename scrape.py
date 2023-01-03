import argparse
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from time import sleep

def scrape_format(args):
  logging.info('beginning scrape_format()')
  cards = ""
  page_counter = 1
  driver = webdriver.Firefox()

  with open('format_abbreviations.json') as file:
    abbreviations = json.load(file)
  abbreviation = abbreviations[args.format]

  with open('format_mappings.json') as file:
    mappings = json.load(file)
  mapping = mappings[args.format][args.timeframe]

  url = f'https://www.mtgtop8.com/topcards?f={abbreviation}&meta={mapping}'
  logging.info('url preparation seems ok: {url}')
  driver.get(url)

  if args.deck == 'side':
    logging.info('attempting to access side deck results')
    md_sb_toggles = driver.find_elements(by=By.NAME, value="maindeck")
    md_sb_toggles[1].click()
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

    # "wait until staleness" isn't cooperating
    # website is being very slow. script inaccurately terminates early
    # temporary "solution": call next page, sleep long time. give chance to load
    #sleep(30)
    WebDriverWait(driver, timeout=10).until(staleness_of(results[0]))

  logging.info('looks like reached end of results')
  return cards

def log_to_file(data, args):
  with open(f'cards_in_{args.format}_{args.deck}board_{args.timeframe}.jsonl', 'w') as file:
    file.write(data)

def parse_args():
  parser=argparse.ArgumentParser(description="a script to scrape mtgtop8 'cards used in a format'")
  parser.add_argument("--format", type=str, default="legacy", choices=['vintage', 'legacy', 'cedh'])  # maybe: 'modern', 'standard', 'pauper'
  parser.add_argument("--deck", type=str, default="main", choices=['main', 'side'])  # site doesn't allow 'simulview both'
  parser.add_argument("--timeframe", type=str, default="all", help="default is 'all'; see format_mappings.json for format-specific options")
  args=parser.parse_args()
  with open('format_mappings.json') as file:
    test = json.load(file)
  try:
    test[args.format][args.timeframe]
  except KeyError:
    logging.critical('invalid timeframe for format; see format_mappings.json for format-specific options')
    exit()
  logging.info('arguments seem parsed')
  return args

def main():
  logging.basicConfig(filename='scrape.log', encoding='utf-8', level=logging.DEBUG)
  arguments = parse_args()  
  scrape_result = scrape_format(arguments)
  log_to_file(scrape_result, arguments)

if __name__ == '__main__':
  main()
