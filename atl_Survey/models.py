# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

from django import forms

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'atl_Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sex = models.IntegerField(initial=None,
                              choices=[(1, 'Femme'), (0, 'Homme')],
                              verbose_name='Sexe',
                              widget=widgets.RadioSelect())
    student = models.IntegerField(initial=None,
                                  choices=[(1, 'Oui'), (0, 'Non')],
                                  verbose_name='Etes-vous étudiant(e)?',
                                  widget=widgets.RadioSelect())
    field_of_studies = models.IntegerField(initial=None,
                                           choices=[(0, 'Economie-Gestion'),
                                                    (1, 'Autres')],
                                           verbose_name='Discipline étudiée (actuellement ou lorsque vous étiez étudiant)?',
                                           widget=widgets.RadioSelect(), blank=True)
    check_partners= models.IntegerField(initial=None,
                                choices=[2,3,4],
                                verbose_name="Au cours de cette expérience, avec combien de chercheurs étiez-vous connecté(e) ?",
                                widget=widgets.RadioSelect())
    check_matching = models.IntegerField(initial=None,
                                choices=[(0,"Oui"), (1,"Non")],
                                verbose_name="Etiez-vous connecté(e) aux mêmes chercheurs pendant l'expérience ?",
                                widget=widgets.RadioSelect())

    check_understanding_incentives = models.IntegerField(initial = None,
                                                         choices=[(1, "Votre score à la fin de l'expérience"),
                                                                  (2, "Votre rang à la fin de l'expérience"),
                                                                  (3, "Votre score ET votre rang à la fin de l'expérience")],
                                                         verbose_name= "D'après les consignes, vous avez compris que vos gains à la fin de l'expérience sont déterminés par: ")

    check_patterns = models.IntegerField(initial = None,
                                         choices=[(1, "par un régle précise que j'ai comprise"),
                                                  (2, "par un régle précise que je n'ai pas entièrement comprise"),
                                                  (3, "de façon aléatoire")],
                                         verbose_name= "D'après votre expérience au cous du jeu, vous avez compris que la découverte de capsules était déterminée: ")

    comments = models.TextField(
        blank=True,
        max_length=3000,
        verbose_name = "Le cas échéant, notez ici les soucis vous avez eus pendant l'expérience (images pas "
                       "chargées ou similaires), merci."

    )
