from twitpy import TwitPy
try:
  import config
except ImportError:
  raise ImportError("Missing config.py. Did you copy it from config.py.dist?")

TwitPy(username=config.USERNAME, password=config.PASSWORD,
  chrome_path=config.CHROME_PATH) \
  .login() \
  .unfollow_users(amount=15) \
  .follow_from_recommended(amount=100) \
  .end()