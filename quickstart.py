from twitpy import TwitPy

TwitPy(username="t_tomgrossmann", password="****") \
  .login() \
  .follow_from_recom(amount=250) \
  .unfollow_users(amount=100) \
  .end()