from otree.api import Currency as c, currency_range
# from .models import Constants
import random

class Participant():
    def __init__(self):
        self.vars = {}
        self.payoff = c(0)

class Constants():
    players_per_group = 4
    auto_traders_per_group = 4
    num_rounds = 1
    endowment = c(50)
    reward = c(20)
    red = 'Red'
    blue = 'Blue'
    trade_good = 'Trade Good'

class Round():
    def __init__(self):
        self.role_pre = None
        self.other_role_pre = None
        self.token_color = None
        self.other_token_color = None
        self.group_color = None
        self.trade_attempted = None
        self.trade_succeeded = None
        self.payoff = None

    def over(self):
        if all(vars(self).values()):
            return True
        return False
    
class AutomatedTrader():
    def __init__(self, session, id_in_group):
        self.participant = Participant()
        self.__round_data = [Round()]
        self.session = session
        self.id_in_group = id_in_group

    def trade(self, subsession):
        # self.session.vars['pairs'] is a list of rounds.
        # each round is a dict of (group,id):(group,id) pairs.
        group_id = self.participant.vars['group']
        player_groups = subsession.get_groups()
        bot_groups = self.session.vars['automated_traders']
        # gets a another pair
        # the other pair is the pair that is paired with the current player
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.id_in_group - 1)]
        if other_group < len(player_groups):
            other_player = player_groups[other_group].get_player_by_id(other_id + 1)
        else:
            other_player = bot_groups[(other_group, other_id)]

        # whatever color token they were assigned in models.py
        self.token_color = self.participant.vars['token']
        self.other_token_color = other_player.participant.vars['token']

        # defining roles as in models.py
        # ensuring opposites, such that half are producers and half are consumers
        self.role_pre = 'Consumer' if self.participant.vars['token'] != Constants.trade_good else 'Producer'
        self.other_role_pre = 'Consumer' if self.other_token_color != Constants.trade_good else 'Producer'

        # defining group color as in models.py
        self.group_color = self.participant.vars['group_color']
        self.other_group_color = other_player.participant.vars['group_color']

        # logic for whether you trade or not. 
        if self.role_pre == self.other_role_pre:
            self.trade_attempted = False
        else:
            self.trade_attempted = True

    def compute_results(self, subsession):
        group_id = self.participant.vars['group'] 
        player_groups = subsession.get_groups()
        bot_groups = self.session.vars['automated_traders']
        
        # identify trading partner
        # similar to above in Trade()
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.id_in_group - 1)]
        
        # get other player object
        if other_group < len(player_groups):
            other_player = player_groups[other_group].get_player_by_id(other_id + 1)
        else:
            other_player = bot_groups[(other_group, other_id)]

        # define initial round payoffs
        round_payoff = c(0)

        # logic for switching objects on trade
        # if both players attempted a trade, it must be true
        # that one is a producer and one is a consumer.
        # Only 1 player performs the switch
        if self.trade_attempted and other_player.trade_attempted: 
            # only 1 player actually switches the goods
            if not self.trade_succeeded:
                # switch tokens
                self.participant.vars['token'] = self.other_token_color
                other_player.participant.vars['token'] = self.token_color
                # set players' trade_succeeded field
                self.trade_succeeded = True
                other_player.trade_succeeded = True
            # give the consumer a payoff
            if self.role_pre == 'Consumer':
                round_payoff = Constants.reward
        else:
            self.trade_succeeded = False

        # penalties for self
        # if your token matches your group color
        if self.participant.vars['token'] == self.participant.vars['group_color']:
            round_payoff -= c(self.session.config['token_store_cost_homogeneous'])

        # if your token matches the opposite group color
        elif self.participant.vars['token'] != Constants.trade_good:
            round_payoff -= c(self.session.config['token_store_cost_heterogeneous'])

        # set payoffs
        self.set_payoffs(round_payoff)
    
    def set_payoffs(self, round_payoff):
        self.payoff = round_payoff

    @property
    def payoff(self):
        r = self.__round_data[-1]
        return r.payoff

    @payoff.setter
    def payoff(self, v):
        self.__check_round_over()
        self.__round_data[-1].payoff = v
        self.participant.payoff += v
    
    def __check_round_over(self):
        r = self.__round_data[-1]
        if r.over():
            self.round_data.append(Round())
    
    def in_round(self, n):
        return self.__round_data[n - 1]

    @property
    def round_number(self):
        return len(self.__round_data)
    
    @property
    def role_pre(self):
        r = self.__round_data[-1]
        return r.role_pre

    @role_pre.setter
    def role_pre(self, v):
        self.__check_round_over()
        self.__round_data[-1].role_pre = v

    @property
    def other_role_pre(self):
        r = self.__round_data[-1]
        return r.other_role_pre

    @other_role_pre.setter
    def other_role_pre(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_role_pre = v
    
    @property
    def token_color(self):
        r = self.__round_data[-1]
        return r.token_color

    @token_color.setter
    def token_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].token_color = v

    @property
    def other_token_color(self):
        r = self.__round_data[-1]
        return r.other_token_color

    @other_token_color.setter
    def other_token_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_token_color = v

    @property
    def group_color(self):
        r = self.__round_data[-1]
        return r.group_color

    @group_color.setter
    def group_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].group_color = v

    @property
    def other_group_color(self):
        r = self.__round_data[-1]
        return r.other_group_color

    @other_group_color.setter
    def other_group_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_group_color = v

    @property
    def trade_attempted(self):
        r = self.__round_data[-1]
        return r.trade_attempted

    @trade_attempted.setter
    def trade_attempted(self, v):
        self.__check_round_over()
        self.__round_data[-1].trade_attempted = v

    @property
    def trade_succeeded(self):
        r = self.__round_data[-1]
        return r.trade_succeeded

    @trade_succeeded.setter
    def trade_succeeded(self, v):
        self.__check_round_over()
        self.__round_data[-1].trade_succeeded = v

