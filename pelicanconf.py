#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Yusuke Tsutsumi'
SITENAME = 'toumorokoshi'
SITEURL = '.'
TAGLINE = 'Yusuke Tsutsumi'
# THEME = "pelican-bootstrap3"
STATIC_PATHS = ('images', 'static')
THEME = '/home/tsutsumi/workspace/pelican-bootstrap3/'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Blogroll
# MENUITEMS = (('GitHub', 'https://github.com/toumorokoshi'),
#              ('StackOverflow', 'http://stackoverflow.com/users/288570/drakeanderson'))

# Social widget
SOCIAL = (('GitHub', 'https://github.com/toumorokoshi'),
          ('StackOverflow', 'http://stackoverflow.com/users/288570/drakeanderson'),
          ('LinkedIn', 'http://www.linkedin.com/profile/view?id=56043626'))

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
GITHUB_SKIP_FORK = 3
GITHUB_SHOW_USER_LINK = 3
BOOTSTRAP_THEME = 'yeti'

DISPLAY_PAGES_ON_MENU = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

SHOW_ABOUTME = True
AVATAR = "/images/profile.png"
ABOUT_ME = """ 
Jack of some trades. Interested in build systems, testing,
programming language design, and text editors.  
<br/>
<br/>
I work at Zillow.
"""
