"""Module only used for the unfollow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys

def unfollow_users(browser, amount):
  """Unfollows given amount of users"""

  unfollowed = 0
  last_length = 0

  #Click on the view all button on the main page to load all the recommended accounts
  browser.get('https://twitter.com/following')

  body_elem = browser.find_element_by_tag_name('body')

  timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Following')]")

  # Make visible enough follow buttons
  while len(timeline) < amount and len(timeline) > last_length:
    last_length = len(timeline)
    body_elem.send_keys(Keys.END)
    sleep(1)
    body_elem.send_keys(Keys.HOME)
    sleep(1)

    #browser.execute_script("window.scroll(0, document.documentElement.scrollTop + 150)") 

    timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Following')]")

  if len(timeline) > amount:
    unfollowed = amount
  else:
    unfollowed = len(timeline)


  # Click on the buttons
  for index, button in enumerate(timeline[:unfollowed]):
    action_chain = Actions(browser)
    action_chain.move_to_element(button)
    action_chain.wait(1)
    action_chain.move_to_element(button)
    action_chain.click()
    action_chain.wait(1)

    confirm_button = browser.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']//span[contains(text(),'Unfollow')]")
    
    action_chain.move_to_element(confirm_button)
    action_chain.click()
    action_chain.wait(1)
    action_chain.print_it(str(index + 1) + '/' + str(unfollowed))
    action_chain.perform()

  return unfollowed