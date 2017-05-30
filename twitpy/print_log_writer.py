"""Module only used to log the number of followers to a file"""
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

def log_follower_num(browser, username):
  """Prints and logs the current number of followers to
  a seperate file"""
  browser.get('https://www.twitter.com/' + username)

  followed_by = browser.find_element_by_xpath('//a[@data-nav ="followers"]/span[@class="ProfileNav-value"]').text

  with open('./logs/followerNum.txt', 'a') as numFile:
    numFile.write('{:%Y-%m-%d %H:%M} {}\n'.format(datetime.now(), followed_by or 0))
