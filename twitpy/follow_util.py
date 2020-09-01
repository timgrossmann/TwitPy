"""Module only used for the follow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


class FollowUtil:
    def __init__(self, browser, amount, delay_click=6, num_discovery_retries=1, discovery_retry_delay=1, logger=None, debug=False):
        self.browser = browser
        self.amount = amount
        self.num_discovery_retries = num_discovery_retries
        self.discovery_retry_delay = discovery_retry_delay
        self.logger = logger
        self.debug = debug
        self.num_followed = 0
        self.delay_click=delay_click

    def follow_from_recommended(self):
        """Follows given amount of users from the who to follow list"""
        self.browser.get("https://twitter.com/i/connect_people")  #  maybe it's useful for something passing user_id param ?
        self.num_followed = 0
        while self.num_followed < self.amount:

            discovery = self.discover()

            if self.logger and self.debug:
                self.logger.debug("Performing follow")
            try:
                self.perform_follow(discovery)  #  Sometimes it clicks the user instead of the button.
            except StaleElementReferenceException:
              self.browser.get("https://twitter.com/i/connect_people")
              if self.logger:
                self.logger.info("Miss click. Going back to recommendations")
              continue

            if self.logger and self.debug:
                self.logger.debug("Reloading the page")
            self.browser.refresh()  # Twitter seems to have disabled the infinite scroll by 2020.

        if self.logger and self.debug:
            self.logger.info("Finished follow discovery successfully")
        return self.num_followed

    def discover(self):
        num_discovery = 0
        # while num_discovery < (self.amount - self.num_followed):
        retry_i = 0
        while retry_i < self.num_discovery_retries:
            # self.__updown()
            discovery = self.browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Follow')]")
            if len(discovery) > num_discovery:
                retry_i = 0
                num_discovery = len(discovery)
                if self.logger and self.debug:
                    self.debug("Discovered {} new followable accounts".format(len(num_discovery) - num_discovery))
                continue
            if num_discovery >= (self.amount - self.num_followed):
                if self.logger and self.debug:
                    self.debug("Discovered all the remaining necessary accounts")
                break
            retry_i += 1
            self.logger.debug("Couldn't load more followable elements. Retrying {}/{}".format(retry_i, self.num_discovery_retries))
        else:
            if self.logger and self.debug:
                self.logger.debug("Finished following loop due to the browser not loading more followable elements")
        # break
        # else:
        #     if self.logger and self.debug:
        #         self.logger.debug("Finished follow discovery ROUND successfully")
        return discovery

    def perform_follow(self, discovery):
        for index, button in enumerate(discovery):
            action_chain = Actions(self.browser)
            action_chain.move_to_element(button)
            action_chain.wait(1)
            action_chain.click()
            action_chain.wait(self.delay_click)
            # action_chain.print_it(str(index + 1) + "/" + str(followed))
            action_chain.perform()
            self.num_followed += 1

    # def __updown(self):
    #     body_elem = self.browser.find_element_by_tag_name("body")
    #     body_elem.send_keys(Keys.END)
    #     sleep(2)
    #     body_elem.send_keys(Keys.HOME)
    #     sleep(2)

