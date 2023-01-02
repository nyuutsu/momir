from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

def scrape_test(test_flag):
  cards = ""
  #page_counter = 1
  
  """
  there are 45 pages of "topcards?f=LE&meta=39".
  the full dataset only needs to be scraped once
  for testing scraping "just the last bit" is fine
  `test_flag` modifies the counter used in "go to the next page" requests
  to make the first one skip ahead to e.g. page 43 of 45
  """
  page_counter = test_flag
  driver = webdriver.Firefox()

  # last two months of cards in mainboards >= 0.1%
  driver.get("https://www.mtgtop8.com/topcards?f=LE&meta=39")

  # all time cards in mainboards >= 0.1%
  #driver.get("https://www.mtgtop8.com/topcards?f=LE&meta=16")
  
  # TODO: sideboard mode, format + duration flags

  while driver.find_elements(by=By.CLASS_NAME, value="L14"):
    
    print(f'🮐🮐🮐🮐🮐 Page {page_counter} Start 🮐🮐🮐🮐🮐')

    results = driver.find_elements(by=By.CLASS_NAME, value="L14")
    
    for k, v in enumerate(results):
      if k % 3 == 0:
        cards += f'{v.text}\n'
        print(v.text)
    
    print(f'🮐🮐🮐🮐🮐 Page {page_counter} End 🮐🮐🮐🮐🮐')
        
    page_counter = page_counter + 1
    
    driver.execute_script(f'PageSubmit({page_counter})')
    WebDriverWait(driver, timeout=5).until(staleness_of(results[0]))

  with open('cards_in_legacy.jsonl', 'w') as file:
    file.write(cards)


def main():
  scrape_test(test_flag = 43)

if __name__ == '__main__':
  main()