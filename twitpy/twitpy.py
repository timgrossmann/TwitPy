"""OS Modules environ method to get the setup vars from the Environment"""
from datetime import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .utils import get_logger, parse_args
from .login_util import login_user
from .print_log_writer import log_follower_num
from .follow_util import FollowUtil
from .unfollow_util import UnfollowUtil

LOGGER = get_logger()
ARGS = parse_args()

class TwitPy:
    """Class to be instantiated to use the script"""

    def __init__(self, username=None, password=None, nogui=False, chrome_path="./assets/chromedriver"):
        if nogui:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

        chrome_options = Options()
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--lang=en-US")
        chrome_options.add_experimental_option("prefs", {"intl.accept_languages": "en-US"})

        # managed_default_content_settings.images = 2: Disable images load, this setting can improve pageload & save bandwidth
        # default_content_setting_values.notifications = 2: Disable notifications
        # credentials_enable_service & password_manager_enabled = false: Ignore save password prompt from chrome
        chrome_prefs = {
            "intl.accept_languages": "en-US",
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile": {"password_manager_enabled": False},
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)

        self.browser = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        self.browser.implicitly_wait(5)

        self.logFile = open("./logs/logFile.txt", "a+")
        self.logFile.write("Session started - %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        if not username or not password:
            LOGGER.info("Please provide Username and Password")
            return

        self.username = username
        self.password = password
        self.nogui = nogui

        self.followed = 0

        self.ignore_users = []

        self.aborting = False

    def login(self):
        """Used to login the user either with the username and password"""
        LOGGER.info("Logging in...")
        if not login_user(self.browser, self.username, self.password):
            LOGGER.info("Wrong login data!")
            self.logFile.write("Wrong login data!\n")

            self.aborting = True
        else:
            LOGGER.info("Logged in successfully!")
            self.logFile.write("Logged in successfully!\n")

        try:
            # get the username from the logo image link, in case we log in with the email.
            profile_logos = self.browser.find_elements_by_xpath("//div[@style='flex-basis: 49px;']//a")
            self.username = profile_logos[0].get_attribute("href").split("/")[-1]
        except IndexError:
            pass

        log_follower_num(self.browser, self.username)

        return self

    def follow_from_recommended(self, amount=50):
        """Follows given amount of users from the 'Who to follow' list"""

        if self.aborting:
            return self

        followed = amount

        follow_util = FollowUtil(self.browser, amount, logger=LOGGER, debug=ARGS.debug)

        while followed > 0:
            new_followed = follow_util.follow_from_recommended()

            if new_followed == 0:
                print("Aborting because no recommendations left")
                self.logFile.write("Aborting because no recommendations left\n")
                break

            followed -= new_followed

            LOGGER.info("New followed {}".format(new_followed))


        self.followed += followed

        return self

    def unfollow_users(self, amount=50):
        """Unfollows given amount of users"""

        if self.aborting:
            return self

        to_unfollow = amount
        unfollow_util = UnfollowUtil(self.browser, amount, logger=LOGGER, debug=ARGS.debug)

        while to_unfollow > 0:
            new_unfollowed = unfollow_util.unfollow_users()

            if new_unfollowed == 0:
                break

            to_unfollow -= new_unfollowed

            LOGGER.info("New unfollowed {}".format(new_unfollowed))

        return self

    def end(self):
        """Closes the current session"""
        self.browser.delete_all_cookies()
        self.browser.close()

        if self.nogui:
            self.display.stop()

        LOGGER.info("")
        LOGGER.info("Session ended")
        LOGGER.info("-------------")

        self.logFile.write("\nSession ended - {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.logFile.write("-" * 20 + "\n\n")
        self.logFile.close()

        with open("./logs/followed.txt", "w") as followFile:
            followFile.write(str(self.followed))
