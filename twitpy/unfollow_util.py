"""Module only used for the unfollow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


class UnfollowUtil:
    def __init__(self, browser, amount, delay_click=6, num_discovery_retries=1, discovery_retry_delay=1, logger=None, debug=False):
        self.browser = browser
        self.amount = amount
        self.num_discovery_retries = num_discovery_retries
        self.discovery_retry_delay = discovery_retry_delay
        self.logger = logger
        self.debug = debug
        self.num_unfollowed = 0
        self.delay_click = delay_click

    def unfollow_users(self):
        """Follows given amount of users from the who to unfollow list"""
        self.browser.get("https://twitter.com/following")  #  maybe it's useful for something passing user_id param ?
        self.num_unfollowed = 0
        while self.num_unfollowed < self.amount:

            discovery = self.discover()

            if self.logger and self.debug:
                self.logger.debug("Performing unfollow")
            try:
                self.perform_unfollow(discovery)  #  Sometimes it clicks the user instead of the button.
            except StaleElementReferenceException:
                self.browser.get("https://twitter.com/following")
                if self.logger:
                    self.logger.info("Miss click. Going back to recommendations")
                continue
            except NoSuchElementException:
              if self.logger:
                self.logger.info("Didnt found any unfollowable item, skipping")
              return 0

            if self.logger and self.debug:
                self.logger.debug("Reloading the page")
            self.browser.refresh()  # Twitter seems to have disabled the infinite scroll by 2020.

        if self.logger and self.debug:
            self.logger.info("Finished unfollow discovery successfully")
        return self.num_unfollowed

    def discover(self):
        num_discovery = 0
        # while num_discovery < (self.amount - self.num_unfollowed):
        retry_i = 0
        while retry_i < self.num_discovery_retries:
            # self.__updown()
            discovery = self.browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Following')]")
            if len(discovery) > num_discovery:
                retry_i = 0
                num_discovery = len(discovery)
                if self.logger and self.debug:
                    self.debug("Discovered {} new unfollowable accounts".format(len(num_discovery) - num_discovery))
                continue
            if num_discovery >= (self.amount - self.num_unfollowed):
                if self.logger and self.debug:
                    self.debug("Discovered all the remaining necessary accounts")
                break
            retry_i += 1
            self.logger.debug("Couldn't load more unfollowable elements. Retrying {}/{}".format(retry_i, self.num_discovery_retries))
        else:
            if self.logger and self.debug:
                self.logger.debug("Finished unfollowing loop due to the browser not loading more unfollowable elements")
        # break
        # else:
        #     if self.logger and self.debug:
        #         self.logger.debug("Finished unfollow discovery ROUND successfully")
        return discovery

    def perform_unfollow(self, discovery):
        for _, button in enumerate(discovery):
            action_chain = Actions(self.browser)
            action_chain.move_to_element(button)
            action_chain.wait(1)
            action_chain.move_to_element(button)
            action_chain.click()
            action_chain.wait(self.delay_click)
            action_chain.perform()

            confirm_button = self.browser.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']//span[contains(text(),'Unfollow')]")

            action_chain = Actions(self.browser)
            action_chain.move_to_element(confirm_button)
            action_chain.click()
            action_chain.wait(1)
            # action_chain.print_it(str(index + 1) + '/' + str(unfollowed))
            action_chain.perform()

            self.num_unfollowed += 1

    # def __updown(self):
    #     body_elem = self.browser.find_element_by_tag_name("body")
    #     body_elem.send_keys(Keys.END)
    #     sleep(2)
    #     body_elem.send_keys(Keys.HOME)
    #     sleep(2)

