from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Introduction)
        yield (pages.Trade, {
            'trade_attempted': False,
            'role_pre': 'Producer',
            'group_color': 'Red',
            'other_role_pre': 'Consumer',
            'other_group_color': 'Blue',
        })
        yield (pages.Results, {
            'trade_succeeded': False,
            'token_color': None,
            'round_payoff': 0,
        })

