from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class start_experiment(Page):

    def is_displayed(self):
        return self.round_number == 1
    pass

class Consentment(Page):

    def is_displayed(self):
        return self.round_number == 1
    pass

class Welcome(Page):

    def is_displayed(self):
        return self.round_number == 1
    pass

class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1
    pass

class Tutorial_1_MyPage(Page):
    def is_displayed(self):
        return self.round_number == 1
    pass

class Tutorial_2_Results(Page):
    def vars_for_template(self):
        return {
        'degree': self.subsession.degree,
        }
    def is_displayed(self):
        return self.round_number == 1
    pass

class Tutorial_3_Sharing_results(Page):
    def vars_for_template(self):
        return {
        'degree': self.subsession.degree,
        'treatment':self.subsession.matching,
        }
    def is_displayed(self):
        return self.round_number == 1
    pass

class Tutorial_3B_Sharing_results(Page):
    def vars_for_template(self):
        return {
        'degree': self.subsession.degree,
        'treatment':self.subsession.matching,
        }
    def is_displayed(self):
        return self.round_number == 1
    pass

class Tutorial_4_Last_page(Page):
    def is_displayed(self):
        return self.round_number == 1
    pass

class MyPage(Page):
    form_model = models.Player
    form_fields = ['total_score', 'triad', 'active']
    timeout_seconds= 30
    timer_text = ""

    def vars_for_template(self):
        listed_grid = self.subsession.get_grid_list()
        listed_values_grid = self.subsession.get_grid_values_list()

        if self.player.in_round(self.subsession.round_number).accrued_bonuses >0:
            stringed_capsule = self.subsession.capsule_sequence
            print("SONO IN VIEWS CAPSULE %%%%%%%%%%%%%%%% ", (stringed_capsule))
            stringed_capsule = self.subsession.capsule_sequence.split(',')
            print("SONO IN VIEWS CAPSULE SPLIT %%%%%%%%%%%%%%%% ", (stringed_capsule))
            #stringed_capsule = [l.strip('\n') for l in stringed_capsule]
            capsule_actual = stringed_capsule[self.player.accrued_bonuses-1].split(' ')[1]
            print("SONO IN VIEWS CAPSULE 2 %%%%%%%%%%%%%%%% ", capsule_actual)
        else:
            capsule_actual = "nothing.png"
        return {
            'k_multiplicator': self.player.k_multiplicator,
            'num_round': self.round_number,
            'total_num_round': Constants.num_rounds,
            'player_id': self.player.id_in_group,
            'pic_1': 'potions/'+listed_grid[1],
            'pic_2': 'potions/'+listed_grid[2],
            'pic_3': 'potions/'+listed_grid[3],
            'pic_4': 'potions/'+listed_grid[4],
            'pic_5': 'potions/'+listed_grid[5],
            'pic_6': 'potions/'+listed_grid[6],
            'pic_7': 'potions/'+listed_grid[7],
            'pic_8': 'potions/'+listed_grid[8],
            'pic_9': 'potions/'+listed_grid[9],
            'pic_10': 'potions/'+listed_grid[10],
            'pic_11': 'potions/'+listed_grid[11],
            'pic_12': 'potions/'+listed_grid[12],
            'pic_13': 'potions/'+listed_grid[13],
            'pic_14': 'potions/'+listed_grid[14],
            'pic_15': 'potions/'+listed_grid[15],
            'pic_16': 'potions/'+listed_grid[16],
            'v_1': listed_values_grid[1],
            'v_2': listed_values_grid[2],
            'v_3': listed_values_grid[3],
            'v_4': listed_values_grid[4],
            'v_5': listed_values_grid[5],
            'v_6': listed_values_grid[6],
            'v_7': listed_values_grid[7],
            'v_8': listed_values_grid[8],
            'v_9': listed_values_grid[9],
            'v_10': listed_values_grid[10],
            'v_11': listed_values_grid[11],
            'v_12': listed_values_grid[12],
            'v_13': listed_values_grid[13],
            'v_14': listed_values_grid[14],
            'v_15': listed_values_grid[15],
            'v_16': listed_values_grid[16],
            'capsule_image': 'capsules/'+capsule_actual

        }
    def before_next_page(self):
        if self.timeout_happened:
            # assign bot variable (BOT is playing)
            self.player.BOT_combination = 1

            # define random choice of the bot
            ## define random numbers used to define trio (values + letters)
            numbers = range(1,16)
            sampled = random.sample(numbers, 3)
            ## define letters set - first value not considered because of structure of values grid (see txt)
            objects = ["","A", "B", "C", "D", "E", "F", "G", "H", "I", "L", "M", "N", "O", "P", "Q", "R"]
            ## define values set (first value not considered - it says the round num)
            listed_values_grid = self.subsession.get_grid_values_list()
            ## choice of i) values ii) letters
            list_values = [listed_values_grid[sampled[0]], listed_values_grid[sampled[1]], listed_values_grid[sampled[2]]]
            list_objects = [objects[sampled[0]], objects[sampled[1]], objects[sampled[2]]]
            print("BOT CHOICE::: INFO YOU NEED %%%%%%%%%%%%%%%%","the values ", listed_values_grid,"the samples ",sampled,
                  "the chosen values ", list_values,"the letters associated ", list_objects,"the payoff ",sum(list_values))
            # pass values
            self.player.triad = ''.join(list_objects)
            self.player.total_score = sum(list_values) + 3*self.player.k_multiplicator
        self.player.check_combos()
        self.player.accrue_score()


    pass

class ResultsWaitPage(WaitPage):
    title_text = "Page d'attente"
    body_text = "S'il vous plait, attendez les autres participants"
    pass

class Results(Page):
    form_model = models.Player
    form_fields = ['share_decision']
    timeout_seconds = 30
    timer_text = ""

    def vars_for_template(self):

        # compute the evolution of the ranking
        ranking_evolution = -999
        if self.subsession.round_number > 1:
            ranking_evolution = self.player.in_round(self.subsession.round_number-1).ranking - self.player.in_round(self.subsession.round_number).ranking
            print("EVOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", ranking_evolution)

        # find the image of the capsule based on your accrued bonus
        if self.player.in_round(Constants.num_rounds).accrued_bonuses > 0:
            #stringed_capsule = self.subsession.capsule_sequence
            stringed_capsule = self.subsession.capsule_sequence.split(',')
            capsule_actual = stringed_capsule[self.player.in_round(Constants.num_rounds).accrued_bonuses - 1].split(' ')[1]
        else:
            capsule_actual = "nothing.png"

            pass
        return {
            'total_score': int(self.player.total_score),
            'cumulated_score': int(self.player.accrued_score),
            'k_multiplicator': self.player.k_multiplicator+1,
            'bonus': self.player.bonus_flag,
            'player_id': self.player.id_in_group,
            'evo': ranking_evolution,
            'degree': self.subsession.degree,
            'capsule_image':'capsules/'+capsule_actual

        }
    def before_next_page(self):
        if self.timeout_happened:
            # notice: it applies to anyone, irrespective to whether they found bonus or not
            self.player.share_decision=1
            self.player.BOT_sharing = 1
        if self.player.bonus_flag == 1:
            self.player.share_bonus()

    pass

class waitingPage(WaitPage):
    title_text = "Page d'attente"
    body_text = "Merci d'attendre les autres participants"

    def after_all_players_arrive(self):
        self.subsession.define_ranking()
        self.subsession.capsule_order()
        pass

class Sharing_results(Page):
    timeout_seconds = 30
    timer_text = ""

    def vars_for_template(self):
        info = []
        neighbors_list = self.player.neighbors.split(',')
        for i in neighbors_list:
            neighbor = self.group.get_player_by_id(i)
            info.append((neighbor.bonus_flag, neighbor.share_decision))

        print("THIS IS INFOOOOOOOOOOOOOOOO %%%%%%%%%%%%%%%%%%%%%% ", info)
        total_bonus = sum([i[0] for i in info])
        print("THIS IS TOTAL_BONUS %%%%%%%%%%%%%%%%%%%%%% ", total_bonus)
        total_share = len([i for i in info if (i[0]==1) & (i[1]==1)])
        print("THIS IS TOTAL_SHARE %%%%%%%%%%%%%%%%%%%%%% ", total_share)

        return {
            'total_score': self.player.total_score,
            'k_multiplicator': self.player.k_multiplicator+1,
            'reception_bonus': self.player.reception_flag,
            'total_bonuses':total_bonus,
            'total_shared':total_share,
            'degree': self.subsession.degree,
            'treatment':self.subsession.matching
        }
    def before_next_page(self):
        self.player.compute_final_score()

class FinalPage(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self):
        return {
        'cumulated_score': int(self.player.accrued_score),
        'rank': self.player.ranking,
        'session': self.session.code,
        'paid': self.player.in_round(1).paid_player,
        'ID': self.participant.id_in_session
        }

    pass

page_sequence = [
    start_experiment,
    Consentment,
    Tutorial_1_MyPage,
    Tutorial_2_Results,
    Tutorial_3_Sharing_results,
    Tutorial_3B_Sharing_results,
    Tutorial_4_Last_page,
    MyPage,
    waitingPage,
    Results,
    ResultsWaitPage,
    Sharing_results,
    #FinalPage
]

