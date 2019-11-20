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
        self.payoff = c(0)

    def trade(self, other_player):
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1

        #FIX THIS
        # cannot use group_id for indices
        # group id for players is eithr 0 or 1
        # group id for traders is either 3 or 4
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.id_in_group - 1)]
       
        # get states before submitting any forms
        self.group_color = self.participant.vars['group_color']
        self.token_color = self.participant.vars['token']
        self.other_token_color = other_player.participant.vars['token']
        self.role_pre = 'Consumer' if self.token_color != Constants.trade_good else 'Producer'
        self.other_role_pre = 'Consumer' if self.other_token_color != Constants.trade_good else 'Producer'

        # logic for whether you trade or not. 
        if self.role_pre == self.other_role_pre:
            self.trade_attempted = False
        else:
            self.trade_attempted = True if random.random() < 0.8 else False

    def compute_results(self):
        # identify trading partner
        group_id = 0 if self.player.participant.vars['group_color'] == Constants.red else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        # get other player object
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        # define initial round payoffs
        round_payoff = c(0)
        # logic for switching objects on trade
        # if both players attempted a trade, it must be true
        # that one is a producer and one is a consumer.
        # Only 1 player performs the switch
        if self.trade_attempted and other_player.trade_attempted: 
            # give the consumer a payoff
            if self.role_pre == 'Consumer':
                round_payoff = Constants.reward
        else:
            self.trade_succeeded = False
        # penalties for self
        if self.participant.vars['token'] == self.participant.vars['group_color']:
            round_payoff -= c(self.session.config['token_store_cost_homogeneous'])
        elif self.participant.vars['token'] != Constants.trade_good:
            round_payoff -= c(self.session.config['token_store_cost_heterogeneous'])
        # set payoffs
        self.set_payoffs(round_payoff)
    
    def set_payoffs(self, round_payoff):
        self.payoff = round_payoff

#    @payoff.setter
#    def payoff(self, v):
#        self.payoff = v
#        self.participant.payoff += v
    
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

