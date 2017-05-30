"""OS Modules environ method to get the setup vars from the Environment"""
from datetime import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .login_util import login_user
from .print_log_writer import log_follower_num
from .follow_util import follow_from_recommended
from .unfollow_util import unfollow_users

class TwitPy:
  """Class to be instantiated to use the script"""
  def __init__(self, username=None, password=None, nogui=False):
    if nogui:
      self.display = Display(visible=0, size=(800, 600))
      self.display.start()

    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
    self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)
    self.browser.implicitly_wait(5)

    self.logFile = open('./logs/logFile.txt', 'a')
    self.logFile.write('Session started - %s\n' \
                       % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    if not username or not password:
      print('Please provide Username and Password')
      return

    self.username = username
    self.password = password
    self.nogui = nogui

    self.followed = 0

    self.ignore_users = []

    self.aborting = False

  def login(self):
    """Used to login the user either with the username and password"""
    if not login_user(self.browser, self.username, self.password):
      print('Wrong login data!')
      self.logFile.write('Wrong login data!\n')

      self.aborting = True
    else:
      print('Logged in successfully!')
      self.logFile.write('Logged in successfully!\n')

    log_follower_num(self.browser, self.username)

    return self

  def follow_users(self, amount=50):
    """Follows given amount of users from the 'Who to follow' list"""

    if self.aborting:
      return self

    followed = amount

    while followed > 0:
      followed -= follow_from_recommended(self.browser, followed)

    self.followed += amount

    return self

  def unfollow_users(self, amount=50):
    """Unfollows given amount of users"""

    if self.aborting:
      return self

    unfollow_users(self.browser, amount)

    return self

  def end(self):
    """Closes the current session"""
    self.browser.delete_all_cookies()
    self.browser.close()

    if self.nogui:
      self.display.stop()

    print('')
    print('Session ended')
    print('-------------')

    self.logFile.write(
      '\nSession ended - {}\n'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      )
    )
    self.logFile.write('-' * 20 + '\n\n')
    self.logFile.close()

    with open('./logs/followed.txt', 'w') as followFile:
      followFile.write(str(self.followed))
