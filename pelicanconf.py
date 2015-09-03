#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Yusuke Tsutsumi'
SITENAME = 'y.tsutsumi.io'
SITEURL = '.'
TAGLINE = 'Yusuke Tsutsumi'
# THEME = "pelican-bootstrap3"
STATIC_PATHS = ('images', 'static')
THEME = 'pelican-bootstrap3'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Blogroll
# MENUITEMS = (('GitHub', 'https://github.com/toumorokoshi'),
#              ('StackOverflow', 'http://stackoverflow.com/users/288570/drakeanderson'))

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/toumorokoshi'),
    ('Google+', 'https://plus.google.com/+YusukeTsutsumi/'),
    ('LinkedIn', 'http://www.linkedin.com/profile/view?id=56043626')
)

# LINKS = (('', ''),)

DEFAULT_PAGINATION = 10

TAG_CLOUD_MAX_ITEMS = 5

# More configuration related
DISQUS_SITENAME = 'tsutsumi'
GOOGLE_ANALYTICS = 'UA-29270527-2'
# rss
FEED_RSS = 'rss'
# TAG_FEED_RSS = 'rsstag'
# CATEGORY_FEED_RSS = 'rsscategory'
# atom
#FEED_ATOM = 'atom'


DISPLAY_TAGS_ON_SIDEBAR = False

PLUGINS = [
    'pelican_gist'
]

# pelican-bootstrap3 custom options
CUSTOM_CSS = 'static/custom.css'

GITHUB_USER = 'toumorokoshi'
GITHUB_REPO_COUNT = 3
GITHUB_SKIP_FORK = True
GITHUB_SHOW_USER_LINK = True
BOOTSTRAP_THEME = 'yeti'

DISPLAY_PAGES_ON_MENU = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

SHOW_ABOUTME = True
AVATAR = "/images/profile.png"
ABOUT_ME = """
Software Engineer at Zillow. I focus on tools and services for developer
productivity, including build and testing.
<br/>
<br/>
My other interests include programming language design, game development,
and learning languages (the non-programming ones).
"""
