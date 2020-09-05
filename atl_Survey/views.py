# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class FinalPage(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self):
        return {
        'cumulated_score': int(self.participant.vars['app_cumulated_score']),
        'rank': self.participant.vars['app_rank'],
        'session': self.session.code,
        'paid': self.participant.vars['app_paid'],
        'ID': self.participant.label
        }

    pass

class SurveyPage(Page):
    form_model = models.Player
    form_fields = ['sex', #'sisters_brothers',
                   #'religion', 'religion_practice',
                   'student', 'field_of_studies',
                   #'couple',
                   #'boring_task',
                   #'risk_aversion'
                    'check_partners','check_matching', 'check_understanding_incentives', 'check_patterns',
                   'comments']


class MerciPage(Page):
    pass


page_sequence = [
    SurveyPage,
    FinalPage
    # MerciPage
]
