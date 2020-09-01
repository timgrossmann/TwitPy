"""Module only used for the follow part of the script"""
from .actions import Actions
from .time_util import sleep
from selenium.webdriver.common.keys import Keys


def follow_from_recommended(browser, amount, logger=None, debug=False):
    """Follows given amount of users from the who to follow list"""

    followed = 0
    last_length = 0

    # Click on the view all button on the main page to load all the recommended accounts
    browser.get("https://twitter.com/i/connect_people")  #  maybe it's useful for something passing user_id param ?

    body_elem = browser.find_element_by_tag_name("body")

    timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Follow')]")

    if logger and debug:
        logger.debug("Starting Followable elements discovery")

    while len(timeline) < amount:
        last_length = len(timeline)
        body_elem.send_keys(Keys.END)
        sleep(2)
        body_elem.send_keys(Keys.HOME)
        sleep(2)
        timeline = browser.find_elements_by_xpath("//div[@data-testid='UserCell']//span[contains(text(),'Follow')]")
        if len(timeline) <= last_length:
            if logger and debug:
                logger.debug("Finished following loop due to the browser not loading more followable elements")
            break
    else:
        if logger and debug:
            logger.debug("Finished follow discovery successfully")

    if logger and debug:
        logger.debug("Amount: {} - Timeline: {} - Last length: {}".format(amount, len(timeline), last_length))

        # browser.execute_script("window.scroll(0, document.documentElement.scrollTop + 150)")

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
        action_chain.print_it(str(index + 1) + "/" + str(followed))
        action_chain.perform()

    sleep(1)

    return followed

