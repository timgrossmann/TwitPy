# TwitPy
### Quick and dirty follow/unfollow automation for Twitter.

#### Getting started
```bash
git clone https://github.com/timgrossmann/TwitPy.git
cd TwitPy
pip install .
# or depending on your system
python setup.py install
```

Now edit the `quickstart.py` file to your needs.

#### API
```python
from twitpy import TwitPy

TwitPy(username="****", password="****") \
  .login() \
  # follows up to 250 accounts from your recommendations
  .follow_from_recom(amount=250) \ 
  # unfollows 100 accounts from your following list
  .unfollow_users(amount=100) \ 
  .end()
```
