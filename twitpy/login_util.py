"""Module only used for the login part of the script"""
from .time_util import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def test_twofactor(browser):
  twofactor_container = browser.find_element_by_xpath('//input[@type = "tel"]')  
  if twofactor_container:
      code = input("Enter the 2fa code: ")
      ActionChains(browser).move_to_element(twofactor_container).click().send_keys(code).perform()
      submitButton = browser.find_element_by_xpath('//input[@type = "submit"]')
      ActionChains(browser).move_to_element(submitButton).click().perform()
      return True    
  return False

def login_user(browser, username, password):
  """Logins the user with the given username and password"""
  browser.get('https://twitter.com/login')

  #Enter username and password and logs the user in
  userContainer = browser.find_element_by_xpath('//input[contains(@class, "js-username-field email-input js-initial-focus")]')
  passwordContainer = browser.find_element_by_xpath('//input[@type = "password"]')

  action = ActionChains(browser).move_to_element(userContainer).click().send_keys(username) \
          .send_keys(Keys.TAB).send_keys(password).perform()

  submitButton = browser.find_element_by_xpath('//button[@type = "submit"]')
  action = ActionChains(browser).move_to_element(submitButton).click().perform()

  sleep(2)
  test_twofactor(browser)  
  #Check if user is logged-in (If there's two 'nav' elements)
  prof = browser.find_elements_by_xpath('//div[@class = "DashboardProfileCard-content"]')
  if len(prof) > 0:
    return True
  else:
    return False