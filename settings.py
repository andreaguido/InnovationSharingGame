import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = True
else:
    DEBUG = False

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = '&e^z8*gy22fm=u--^$q-(ex-g=&e4&(p9rj7yl)7!&e!9lbl4e'

DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 1


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""
ROOMS=[
{
    'name': 'ClassRoom',
    'display_name': 'ClassRoom',
},
{
    'name': 'session45',
    'display_name': 'Session 45',
    'participant_label_file': '_rooms/session45.txt',
},
{
    'name': 'session46',
    'display_name': 'Session 46',
    'participant_label_file': '_rooms/session46.txt',
},
{
    'name': 'session33',
    'display_name': 'Session 33',
    'participant_label_file': '_rooms/session33.txt',
},
{
    'name': 'session34',
    'display_name': 'Session 34',
    'participant_label_file': '_rooms/session34.txt',
},
{
    'name': 'session35',
    'display_name': 'Session 35',
    'participant_label_file': '_rooms/session35.txt',
},
{
    'name': 'session36',
    'display_name': 'Session 36',
    'participant_label_file': '_rooms/session36.txt',
},
{
    'name': 'session37',
    'display_name': 'Session 37',
    'participant_label_file': '_rooms/session37.txt',
},
{
    'name': 'session38',
    'display_name': 'Session 38',
    'participant_label_file': '_rooms/session38.txt',
},
{
    'name': 'session39',
    'display_name': 'Session 39',
    'participant_label_file': '_rooms/session39.txt',
},
{
    'name': 'session40',
    'display_name': 'Session 40',
    'participant_label_file': '_rooms/session40.txt',
},
{
    'name': 'session41',
    'display_name': 'Session 41',
    'participant_label_file': '_rooms/session41.txt',
}
]

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    # to use qualification requirements, you need to uncomment the 'qualification' import
    # at the top of this file.
    'qualification_requirements': [],
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.000,
    'participation_fee': 0.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

CHANNEL_ROUTING = 'routing.channel_routing'

SESSION_CONFIGS = [
#    {
#        'name': 'Beliefs_game',
#        'display_name': "Labour Market Game",
#        'app_sequence': ['Andy'],
#        'num_demo_participants': 4,
#        'treatment': 0,
#        'matching': 'P',
#        'minimum_wage': 1,
#        'doc': """
#         If treatment = 0, then the shock is negative, if treatment = 1 the shock is positive.
#         if minimum_wage = 0 then FIRING allowed, put 1 otherwise. If matching is PARTNER then put P, otherwise put
#         S for stranger design.
#         """,
#    },
    {
        'name': 'Beliefs_game_asymmetric_info',
        'display_name': "Labour Market Game",
        'app_sequence': ['Andy_asymmetric_info'],
        'num_demo_participants': 4,
        'treatment': 0,
        'online':0,
        'matching': 'P',
        'minimum_wage': 1,
        'doc': """
         If treatment = 0, then the shock is negative, if treatment = 1 the shock is positive.
         If online = 0, then the study is run in the lab. if online = 1, it'll be online.
         if minimum_wage = 0 then FIRING allowed, put 1 otherwise. If matching is PARTNER then put P, otherwise put
         S for stranger design.
         """,
    },
#    {
#        'name': 'Beliefs_game',
#        'display_name': "Labour Market Game - Online",
#        'app_sequence': ['Andy_Online'],
#        'num_demo_participants': 4,
#        'treatment': 0,
#        'matching': 'P',
#        'minimum_wage': 1,
#        'doc': """
#         If treatment = 0, then the shock is negative, if treatment = 1 the shock is positive.
#         if minimum_wage = 0 then FIRING allowed, put 1 otherwise. If matching is PARTNER then put P, otherwise put
#         S for stranger design.
#         """,
#    },
    {
         'name': 'game',
         'display_name': 'game',
         'num_demo_participants': 4,
         'app_sequence': ['game','atl_Survey'],
         'degree': 2,
         'nodes': 4,
         'matching': "P",
         'doc': """
                If matching= P -> partner matching, if treatment = S -> stranger matching
                """
     }
#    {
#        'name': 'public_goods',
#        'display_name': 'Public Goods',
#        'num_demo_participants': 3,
#        'app_sequence': ['public_goods']
#    }

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
