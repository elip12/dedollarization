from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def set_configs(self, prob, homo, hetero):
        assert(prob >= 0.0 and prob <= 1)
        assert(homo >= 0)
        assert(hetero >= 0)
        self.session.config['probability_of_same_group'] = prob
        self.session.config['token_store_cost_homogeneous'] = homo
        self.session.config['token_store_cost_heterogeneous'] = hetero 
    
    def play_round(self):
        case = self.subsession.round_number % 3
        if case == 0:
            self.set_configs(.5, 0, 0)
        elif case == 1:
            self.set_configs(.75, 0, 0)
        else:
            self.set_configs(.75, 1, 2)

        if self.subsession.round_number == 1:
            yield (pages.Introduction)
       
        # get trading partner
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
       
        # get states before submitting any forms
        group_color = self.player.participant.vars['group_color']
        token_color = self.player.participant.vars['token']
        other_token_color = other_player.participant.vars['token']
        role_pre = 'Consumer' if token_color != Constants.trade_good else 'Producer'
        other_role_pre = 'Consumer' if other_token_color != Constants.trade_good else 'Producer'
        payoff = self.player.payoff
        money = self.player.participant.payoff

        # logic for whether you trade or not. 
        if role_pre == other_role_pre:
            trade_attempted = False
            # assert(f'You cannot trade' in self.html)
        else:
            assert(token_color != other_token_color)
            # assert(f'Would you like to offer to trade' in self.html)
            trade_attempted = True if random.random() < 0.8 else False

        # check the html
        # assert(f'Your role is {role_pre}' in self.html)
        # assert(f'Their role is {other_role_pre}' in self.html)


        # play the trading page
        yield (pages.Trade, { 'trade_attempted': trade_attempted })
        # at this point, all fields for the round have been recorded
        # we need to refersh the other_player object
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        other_trade_attempted = other_player.trade_attempted
        
        # Assertion tests
        if trade_attempted and other_trade_attempted:
            assert(self.player.trade_succeeded)
            assert(trade_attempted == self.player.trade_attempted)
            assert(role_pre == self.player.role_pre)
            assert(other_role_pre == self.player.other_role_pre)
            assert(self.player.role_pre != self.player.other_role_pre)
            assert(self.player.token_color != self.player.other_token_color)
        if trade_attempted and not other_trade_attempted:
            assert(not self.player.trade_succeeded)
        if not trade_attempted and other_trade_attempted:
            assert(not self.player.trade_succeeded)
        if not trade_attempted and not other_trade_attempted:
            assert(not self.player.trade_succeeded)

        if not self.player.trade_succeeded:
            assert(self.player.participant.vars['token'] == self.player.token_color)
        if self.player.trade_succeeded:
            #print('PLAYER', group_id, self.player.id_in_group)
            #print(token_color, self.player.token_color)
            #print(other_token_color, self.player.other_token_color)
            #print(self.player.participant.vars['token'])
            assert(self.player.participant.vars['token'] == self.player.other_token_color)
        if self.player.trade_succeeded and self.player.role_pre == 'Consumer':
            assert(self.player.participant.vars['token'] == Constants.trade_good)
            assert(self.player.payoff == Constants.reward)
            assert(self.player.payoff != payoff)
        if self.player.trade_succeeded and self.player.role_pre == 'Producer':
            assert(self.player.participant.vars['token'] == Constants.red \
                or self.player.participant.vars['token'] == Constants.blue)
        if self.player.participant.vars['token'] == group_color:
            assert(self.player.payoff == -(self.session.config['token_store_cost_homogeneous']))
        if self.player.participant.vars['token'] != group_color \
            and self.player.participant.vars['token'] != Constants.trade_good:
            assert(self.player.payoff == -(self.session.config['token_store_cost_heterogeneous']))
        if self.player.participant.vars['token'] == Constants.trade_good:
            assert(self.player.payoff >= 0)
        assert(self.player.participant.payoff == money + self.player.payoff)
    
        # submit the results page
        yield (pages.Results)

