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
        if self.subsession.round_number == 1:
            yield (pages.Introduction)
       

        '''
        if you dont have the option to trade, you should have the same shit you had at the begining
        if you do have the option to trade, and you do trade, and other also trades, you hsould have the opposite thing
        if you do have the option to trade, and you dont trade, you should have same shit
        if you do have option, and other doesnt trade, you should have same shit
        if you trade, you get payoff
        if you have token, you should get penalized by correct amount
        your total money should get updated

        '''

        # get trading partner
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        
        group_color = self.participant.vars['group_color']
        token_color = self.player.participant.vars['token']
        other_token_color = other_player.participant.vars['token']
        role_pre = 'Consumer' if self.player.participant.vars['token'] != Constants.trade_good else 'Producer'
        other_role_pre = 'Consumer' if other_token != Constants.trade_good else 'Producer'
        payoff = self.player.payoff
        money = self.player.participant.payoff

        # logic for whether you trade or not. 
        if role_pre == other_role_pre:
            trade_attempted = False
        else:
            trade_attempted = True if random.random() < 0.5 else False
        # play the trading page
        yield (pages.Trade, { 'trade_attempted': trade_attempted })
        # play the results page
        yield (pages.Results)
        
        # at this point, all fields for the round have been recorded




























