"""Module only used for the follow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys

def follow_from_recommended(browser, amount):
  """Follows given amount of users from the who to follow list"""

  followed = 0
  last_length = 0

  #Click on the view all button on the main page to load all the recommended accounts
  browser.get('https://twitter.com/i/connect_people') # maybe it's useful for something passing user_id param ?

  body_elem = browser.find_element_by_tag_name('body')

  timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Follow')]")

  # Make visible the buttons
  while len(timeline) < amount and len(timeline) > last_length:
    last_length = len(timeline)
    body_elem.send_keys(Keys.END)
    sleep(2)
    body_elem.send_keys(Keys.HOME)
    sleep(2)  

    #browser.execute_script("window.scroll(0, document.documentElement.scrollTop + 150)") 

    timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Follow')]")

  if len(timeline) > amount:
    followed = amount
  else:
    followed = len(timeline)


  # Click the buttons
  for index, button in enumerate(timeline[:followed]):
    action_chain = Actions(browser)
    action_chain.move_to_element(button)
    action_chain.wait(1)
    action_chain.click()
    action_chain.wait(1)
    action_chain.print_it(str(index + 1) + '/' + str(followed))
    action_chain.perform()

  sleep(1)

  return followed