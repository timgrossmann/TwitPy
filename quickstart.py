from twitpy import TwitPy
try:
  import config
except ImportError:
  raise ImportError("Missing config.py. Did you copy it from config.py.dist?")

TwitPy(username=config.USERNAME, password=config.PASSWORD,
  chrome_path=config.CHROME_PATH) \
  .login() \
  .follow_from_recom(amount=5) \
  .unfollow_users(amount=5) \
  .end()