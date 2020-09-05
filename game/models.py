from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from collections import Counter
import itertools, random
import networkx as nx
import numpy as np
import random as rn
import json


author = 'Andrea Guido'

doc = """
Innovation Game
"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 30



class Subsession(BaseSubsession):

    # Define group level vars
    ## settings
    matching = models.CharField()
    degree = models.IntegerField()
    number_of_nodes = models.IntegerField()
    # combos, grid and bonuses
    combos_string = models.CharField()
    bonuses_string = models.CharField()
    grid = models.CharField() # object order
    grid_values = models.CharField() # object values
    capsule_sequence = models.CharField() # the sequence of appearenc of capsules

    # not-saved variables - used for computational reasons
    graph = nx.Graph()

    def creating_session(self):
        self.degree = self.session.config['degree']
        self.number_of_nodes = self.session.config['nodes']
        self.matching = self.session.config['matching']


        if self.round_number == 1:
            # create the network
            self.create_network()

            #shuffle it ONCE for the first
            self.shuffle_network()

            # get grid pictures and values
            self.get_grid()
            self.get_values()

            # get list of capsules
            self.capsule_order()

            # get neighbors
            self.get_neighbors()

            # create combos
            self.define_combinations()

            # choose bonuses
            self.define_bonuses()

            # randomly select players for payment
            self.payment()

        else:

            if self.matching == "P":
                # propagate to other rounds
                # # graph bonuses
                self.graph = self.in_round(1).graph

            else:
                # create a new graph
                self.create_network()
                self.shuffle_network()

            # # neighbors
            self.get_neighbors()

            # get grid pictures and values and capsules
            self.get_grid()
            self.get_values()
            self.capsule_order()

            # # bonuses
            self.combos_string = self.in_round(1).combos_string

            # define new bonuses
            self.define_bonuses()


        pass

    # this function creates the network using Networkx library
    def create_network(self):
        self.graph = nx.watts_strogatz_graph(self.number_of_nodes, self.degree, 0)

        #print('this is the neighbour list of player 1 that is number 0 in the graph%%%%%%%%%', [n for n in self.graph[0]])
        #print('this is the neighbour list of player 1 that is number 0 in the graph%%%%%%%%%', self.graph.neighbors(1))
        #code = self.session.code
        #root = 'edgelist_'
        #path = root+code
        #nx.write_edgelist(self.graph, path='%s.csv' % path, delimiter=';', data=False)
        #for line in nx.generate_edgelist(self.graph, data=False):
        #    print(line)
        #pass

    # this function reshuffles the network each round
    def shuffle_network(self):
        nodes = [i for i in range(self.number_of_nodes)]
        rn.shuffle(nodes)
        adj_list_str = ""
        if self.degree == 4:
            for i in range(0, len(nodes)):
                adj_list = [nodes[i], nodes[(i + 1) % len(nodes)], nodes[(i + 2) % len(nodes)]]
                adj_list_str_temp = ' '.join(map(str, adj_list))
                adj_list_str += adj_list_str_temp + "\n"
        else:
            for i in range(0, len(nodes)):
                adj_list = [nodes[i], nodes[(i + 1) % len(nodes)]]
                adj_list_str_temp = ' '.join(map(str, adj_list))
                adj_list_str += adj_list_str_temp + "\n"
        f = open('adjacency_list.txt', 'w')
        f.write(adj_list_str)
        f.close()

        self.graph = nx.read_adjlist("adjacency_list.txt", nodetype = int, delimiter=" ")

    # this function allows to get neighbours of each player
    def get_neighbors(self):

        for p in self.get_players():
            ids = p.id_in_group - 1
            #print("this is the player in the graph %%%%%%%%%%%% ",ids)
            n = [str(n + 1) for n in self.graph[ids]]
            #print("these are the neighbours of player , ", ids, " : %%%%%%%%%%%% ", n)
            p.neighbors = self.make_string(n)

    # this function allows to transform the string of both objects grid and values into a list which is used in MyPage
    def get_grid_list(self):
        # get grid and put into a list
        stringed_grid = self.grid
        listed_grid = stringed_grid.split(' ')
        listed_grid = [l.strip('\n') for l in listed_grid]
        print("SONO IN VIEWS GRID %%%%%%%%%%%%%%%%% ", (listed_grid))

        return (listed_grid)

    def get_grid_values_list(self):
        # get values of the grid and list it
        stringed_values_grid = self.grid_values
        listed_values_grid = stringed_values_grid.split(' ')
        listed_values_grid = [l.strip('\n') for l in listed_values_grid]
        listed_values_grid = list(map(float, listed_values_grid))
        print("SONO IN VIEWS GRID VALUES %%%%%%%%%%%%%%%% ", (listed_values_grid))

        return (listed_values_grid)

    # this function allows to get the grid of objects
    def get_grid(self):

        file_grid = open('grid.txt', 'r')
        file_lines = file_grid.readlines()
        self.grid = file_lines[self.round_number-1]
        pass

    # this function allows to get the values of each object
    def get_values(self):

        file_grid_values = open('values.txt', 'r')
        file_lines = file_grid_values.readlines()
        self.grid_values = file_lines[self.round_number-1]
        pass

    def capsule_order(self):
        file_grid_values = open('bonus_series.txt', 'r')
        file_lines = file_grid_values.readlines()
        self.capsule_sequence = self.make_string(file_lines)
        pass

    # this function defines the combos
    def define_combinations(self):
        #print("IM in DEFINEE COMBINATIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        # here I define the objects (same names as in the JS) that can be combined
        objects = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "L", "M", "N", "O", "P", "Q", "R"]

        # here I combine them
        combos_temp = list(itertools.combinations([x for x in list(objects)], 3))
        #combos_temp = [x for x in combos_temp_not_usable] #this is to make the variable "usable" through a print
        #print("These are the combos temp", (combos_temp))

        # here I define the variable that records the combinations
        combo = [None] * len(combos_temp)
        #print("This is combo BEFORE FOR %%%%%%%%%%%%%%%%", combo)
        i = 0
        for x in list(combos_temp):
            combo[i] = x[0] + x[1] + x[2]
            i += 1
        #print("These are the combos ", list(combo))

        # save the combos for next round by compressing the variable into a string
        self.combos_string = self.make_string(combo)

        pass


    # here I define the bonuses (randomly chosen)
    def define_bonuses(self):

        # get combos as (list) input
        combo = self.make_list(self.combos_string)

        # define the number of bonuses
        number_of_bonuses = 224

        # randomly draw the bonuses
        bonuses = random.sample(combo, number_of_bonuses)
        #print("These are the bonuses ", list(bonuses))

        # save the bonuses for next round by compressing the variable into a string
        self.bonuses_string = self.make_string(bonuses)
        #print("These are the bonuses STRINGED ", self.bonuses_string)

        pass

    # this function allows to define ranking according to accrued score
    def define_ranking(self):

        # create the tuple
        ranking_list = []
        for p in self.get_players():
            ranking_list.append((p.id_in_subsession, p.accrued_score))

        ranking_list = sorted(ranking_list, key = lambda x:x[1], reverse=True)
        #print("This is the sorted ranking list %%%%%%%%%%%%%%% ", ranking_list)

        # pass on players
        count_ranking = 1
        last_score = 0
        last_rank = 0
        for i in ranking_list:
            #print("this is the player that is being used to record the ranking position %%%%%%%%% ", i[0])
            p = self.get_players()[i[0] - 1]
            if (count_ranking > 1) & (i[1] == last_score):
                p.ranking = last_rank
            else:
                p.ranking = count_ranking
                count_ranking += 1
            last_score = i[1]
            last_rank = p.ranking

    # this function defines the capsule to display based on the accrued bonuses

    # this function allows to transform a list into a long character
    def make_string(self, x):
        return ','.join(x)
        pass

    # this function allows to transform a long character into a list
    def make_list(self, x):
        return x.split(',')
        pass

    def payment(self):
        # randomly select 7 players out of 15 for payment
        paid_players_list = random.sample(self.get_players(), int(self.number_of_nodes/2))
        print("These are the paid players %%%%%%%%%%%%%% ", paid_players_list)

        for p in self.get_players():
            if p in paid_players_list:
                p.paid_player = 1


class Group(BaseGroup):
    pass





class Player(BasePlayer):

    # Input variables - choices from player
    ## this is the combo chosen by the player
    triad = models.CharField()

    ## this is the sharing decision in case of bonus found
    # VALUES CODE: 0 - not sharing; 1 - sharing; -1 - no bonus found (hence no decision)
    share_decision = models.IntegerField(
 initial=1
    )

    # Other variables
    # score-related variables
    total_score = models.FloatField() #score of the round
    accrued_score = models.FloatField() #total accrued score
    #finalpayoff = models.FloatField()
    paid_player = models.FloatField(initial=0) # flag for payment
    # ranking
    ranking = models.IntegerField()
    #bonus-related variables
    ## flags
    bonus_flag = models.IntegerField(initial=0)
    reception_flag = models.IntegerField(initial=0)
    ## count bonus
    k_multiplicator = models.IntegerField(initial=0)
    accrued_bonuses = models.IntegerField(initial=0)
    ## others
    neighbors = models.CharField()
    active = models.IntegerField(initial=0) # flag if player is active on the scren 'MyPage' or not
    BOT_combination = models.IntegerField(initial=0) # flag if bot intervenes
    BOT_sharing = models.IntegerField(initial=0) # flag if player because of BOTs decision (Timeout)

    # this function checks if combination chosen is bonus
    def check_combos(self):
        #print("IM IN CHECKIIIIIIIIIIIIIIIIIIIIING")
        #print("This is multiplicator PRE-BONUS", self.k_multiplicator)

        bonuses = self.subsession.in_round(self.subsession.round_number).bonuses_string
        #print("These are the bonuses DE-STRINGED line 156 %%%%%%%%%%%%%", bonuses)


        # sort triad
        # # unpack
        triad_list = []
        triad_list.extend(self.triad)

        # # sort
        triad_list.sort()
        #print("this is the ordered triad ", triad_list)

        # # pack
        triad_sorted = ''.join(triad_list)

        #print("The condition triad is in bonuses is %%%%%%%%%%%% ", triad_sorted in bonuses)
        if self.subsession.round_number == Constants.num_rounds:
            self.bonus_flag = 1
            self.in_round(Constants.num_rounds).accrued_bonuses = self.accrued_bonuses + 1
            print("I am doing the SCREENSHOT %%%%%%%///\\\%%%%%")
        else:
            print("I am in the normal round checking bonus %%%%%%%%%%%%%||||||||||||||||||%%%%%%%%%%%%%")
            if triad_sorted in bonuses:
                # switch on the flag
                self.bonus_flag = 1

                # accrue bonus
                for z in self.in_rounds(self.round_number + 1, Constants.num_rounds):
                    z.accrued_bonuses = z.accrued_bonuses + 1

                # change the multiplicator for the remaining rounds
                for g in self.in_rounds(self.round_number + 1, Constants.num_rounds):
                    g.k_multiplicator = g.k_multiplicator + 10
                    print("This is multiplicator AFTER-BONUS", self.in_round(self.round_number+1).k_multiplicator)
    pass


    # this function manages the sharing decisions and the propagation of the bonuses
    def share_bonus(self):
        print("IM IN SHARIIIIIIIIIIIIIIIIING BONUS")

        # if the player has found a bonus && decided to share it
        if self.bonus_flag == 1 and self.share_decision == 1:
            print('Im in the IF CONDITION LINE 65 %%%%%%%%%%%%%%%%%%%%%%')
            # get ID of innovator
            id_of_player = self.id_in_group
            print("THIS IS THE ID OF THE INNOVATOR  %%%%%%%%%%%%%%%", id_of_player)

            # get ID of his neighbours
            neighbors_list = self.neighbors.split(',')
            print("this is the list of neighbours %%%%%%%%%%%%%", neighbors_list)

            for i in neighbors_list:
                neighbor = self.group.get_player_by_id(i)
                # swithc on the flag
                neighbor.reception_flag = 1
                # increase multiplicator NOTE!!! from the next round!!!
                for pp in neighbor.in_rounds(self.subsession.round_number+1, Constants.num_rounds):
                    pp.k_multiplicator = pp.k_multiplicator+10
                    # accrue bonus
                    pp.accrued_bonuses = pp.accrued_bonuses + 1
                    print("#################### JE SUIS DANS SHARE BONUS ####################")

    pass

    # this function cumulates the score over rounds
    def accrue_score(self):

        if self.round_number == 1:
            self.accrued_score = self.total_score
        else:
            self.accrued_score = self.total_score + self.in_round(self.round_number - 1).accrued_score

        pass

    # this function computes the final payoff including the ranking score
    def compute_final_score(self):
        print("I'M IN COMPUTE FINAL SCORE %%%%%%%%%%%%%%%%%%%%%%%%")
        if self.subsession.round_number == Constants.num_rounds:
            self.participant.vars['app_cumulated_score'] = self.accrued_score
            self.participant.vars['app_rank'] = self.ranking
            self.participant.vars['app_paid'] = self.in_round(1).paid_player
            #print("I am computing the final payoff %%%%%%%%%%%%")
            #self.finalpayoff = self.accrued_score * (1 + (self.subsession.number_of_nodes + 1 - self.ranking)/10)
            #print("It is %%%%%%%%%%%%", self.accrued_score, "TIMES")
        pass
