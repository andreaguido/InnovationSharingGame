# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        self.submit(views.SurveyPage, {'sex': random.randint(0, 1),
                                       'sisters_brothers': random.randint(0, 1),
                                       'religion': random.randint(0, 5),
                                       'religion_practice': random.randint(0, 5),
                                       'student': random.randint(0, 1),
                                       'field_of_studies': random.randint(0, 7),
                                       'level_of_study': random.randint(0, 3),
                                       'couple': random.randint(0, 1),
                                       'previous_participation': random.randint(0, 1),
                                       'boring_task': random.randint(0, 3),
                                       'risk_aversion': random.randint(0, 10)})

    def validate_play(self):
        pass
