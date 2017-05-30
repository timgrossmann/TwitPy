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

  timeline = browser.find_elements_by_xpath(
    '//div[@class = "GridTimeline"]//button[contains(@class, "EdgeButton user-actions-follow-button js-follow-btn follow-button")]')

  while len(timeline) < amount and len(timeline) > last_length:
    last_length = len(timeline)
    body_elem.send_keys(Keys.END)
    sleep(2)
    body_elem.send_keys(Keys.HOME)
    sleep(2)

    timeline = browser.find_elements_by_xpath(
      '//div[@class = "GridTimeline"]//button[contains(@class, "EdgeButton user-actions-follow-button js-follow-btn follow-button")]')

  if len(timeline) > amount:
    followed = amount
  else:
    followed = len(timeline)

  action_chain = Actions(browser)

  for index, button in enumerate(timeline[:followed]):
    action_chain.move_to_element(button)
    action_chain.wait(1)
    action_chain.click()
    action_chain.wait(1)
    action_chain.print_it(str(index + 1) + '/' + str(followed))

  action_chain.perform()

  sleep(1)

  return unfollowed