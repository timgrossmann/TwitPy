"""Module only used for the follow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys

def follow_from_recommended(browser, amount):
  """Follows given amount of users from the who to follow list"""

  followed = 0
  last_length = 0

  #Click on the view all button on the main page to load all the recommended accounts
  browser.get('https://twitter.com/who_to_follow')

  body_elem = browser.find_element_by_tag_name('body')

  timeline = browser.find_elements_by_xpath('//div[@id = "timeline"]/div/div[@class = "stream"]/ol/li/div/div[@class = "follow-bar"]/div/span/button[1]')

  while len(timeline) < amount and len(timeline) > last_length:
    last_length = len(timeline)
    body_elem.send_keys(Keys.END)
    sleep(2)
    body_elem.send_keys(Keys.HOME)
    sleep(2)

    timeline = browser.find_elements_by_xpath(
      '//div[@id = "timeline"]/div/div[@class = "stream"]/ol/li/div/div[@class = "follow-bar"]/div/span/button[1]')

  if len(timeline) > amount:
    followed = amount
  else:
    followed = len(timeline)

  action_chain = Actions(browser)

  for index, button in enumerate(timeline[:followed]):
    print(str(index) + '/' + str(followed))
    action_chain.move_to_element(button)
    action_chain.wait(1)
    action_chain.click()
    action_chain.wait(1)

  action_chain.perform()

  sleep(1)

  return followed