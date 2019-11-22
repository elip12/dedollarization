from otree.api import Currency as c, currency_range
# from .models import Constants
import pandas as pd
import numpy as np
import random

class Participant():
    def __init__(self):
        self.vars = {'group': None}
        self.payoff = c(0)

class Constants():
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

    def export_data(self, players_per_group):
        cols = ['participant.id_in_session',
                'participant.payoff',
                'participant.is_automated',
                'player.id_in_group',
                'player.role_pre',
                'player.other_role_pre',
                'player.token_color',
                'player.other_token_color',
                'player.group_color',
                'player.other_group_color',
                'player.trade_attempted',
                'player.trade_succeeded',
                'player.payoff',
                'group.id_in_subsession',
                'subsession.round_number',
                'session.code',
                ]
        df = {}
        n = len(self.__round_data)
        id_in_session = (self.id_in_group + 1) + (players_per_group * self.participant.vars['group'])
        df[cols[0]] = np.full(n, id_in_session)
        df[cols[1]] = np.array([r.cumulative_payoff for r in self.__round_data])
        df[cols[2]] = np.full(n, 1)
        df[cols[3]] = np.full(n, self.id_in_group + 1)
        df[cols[4]] = np.array([r.role_pre for r in self.__round_data])
        df[cols[5]] = np.array([r.other_role_pre for r in self.__round_data])
        df[cols[6]] = np.array([r.token_color for r in self.__round_data])
        df[cols[7]] = np.array([r.other_token_color for r in self.__round_data])
        df[cols[8]] = np.array([r.group_color for r in self.__round_data])
        df[cols[9]] = np.array([r.other_group_color for r in self.__round_data])
        df[cols[10]] = np.array([r.trade_attempted for r in self.__round_data])
        df[cols[11]] = np.array([r.trade_succeeded for r in self.__round_data])
        df[cols[12]] = np.array([r.payoff for r in self.__round_data])
        df[cols[13]] = np.full(n, self.participant.vars['group'] + 1)
        df[cols[14]] = np.array([i for i in range(n)])
        df[cols[15]] = np.full(n, self.session.code)
        df = pd.DataFrame(df)
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        df.to_csv(f'producer_consumer_{date}_session_{self.session.code}_automated_trader_{id_in_session}.csv')

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

            ### TREATMENT: BOTS ONLY ACCEPT THEIR OWN COLOR

            # if "bots only trading the same color (blue)" treatment is on
            if self.session.config['bots_trade_same_color']:

                # BOT is "self": if the other token is blue, then trade
                if self.other_token_color == self.group_color:
                    self.trade_attempted = True

                # if not, then don't
                else:
                    self.trade_attempted = False

            # if "bots only trading the same color (blue)" treatment is off
            # then just always trade
            else:
                self.trade_attempted = True

    def compute_results(self, subsession, reward):
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

