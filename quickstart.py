from twitpy import TwitPy

TwitPy(username="t_tomgrossmann", password="Hawai1994") \
  .login() \
  .follow_users(amount=100) \
  .end()
