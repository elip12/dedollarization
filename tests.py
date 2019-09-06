from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (pages.Introduction)
        
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        other_token = other_player.participant.vars['token']
        other_group_color = other_player.participant.vars['group_color']
        role_pre = 'Consumer' if self.player.participant.vars['token'] != Constants.trade_good else 'Producer'
        other_role_pre = 'Consumer' if other_token != Constants.trade_good else 'Producer'
        if role_pre == other_role_pre:
            trade_attempted = False
        else:
            trade_attempted = True if random.random() < .8 else False
        yield (pages.Trade, {
            'trade_attempted': trade_attempted,
        })
        yield (pages.Results)

