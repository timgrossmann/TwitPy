from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Tim Grossmann'


requirements = [
    'selenium==2.53.6',
    'clarifai==2.0.20',
    'pyvirtualdisplay'
]

description = ’Twitter Follow Automation Script’

setup(
    name=‘twitter_py’,
    version=__version__,
    author=__author__,
    author_email='contact.timgrossmann@gmail.com',
    url='https://github.com/timgrossmann/TwitPy’,
    py_modules=‘twitpy’,
    description=description,
    install_requires=requirements
)
