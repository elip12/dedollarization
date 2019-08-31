from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage

from .models import Constants
class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    pass

class Trade(Page):
    form_model = 'player'
    form_fields = [
        'role_pre',
        'trade_attempted',
    ]

    def vars_for_template(self):
        return {
            'role_pre': self.player.participant.vars['role']
        }

    form_fields = [
        'role_post',
        'token_color',
        'trade_succeeded',
        'group_color',
        'round_payoff',
    ]

class ResultsWaitPage(WaitPage):
    body_text = "Waiting for other participants to decide."

    def vars_for_template(self):
        return {
            'role_pre': self.player.participant.vars['role'],
            'trade_attempted': self.player.trade_attempted,
            'initial_token_color': self.player.participant.vars['token_color'],
            'group_color': self.player.participant.vars['group_color'],
        }

    def after_all_players_arrive(self):
        self.player.set_payoffs()

class Results(Page):
        def vars_for_template(self):
            return {
                'trade_succeeded': self.player.trade_succeeded,
                'new_token_color': self.player.participant.vars['token_color'],
                'round_payoff': self.player.round_payoff,
            }

page_sequence = [
    Introduction,
    Trade,
    ResultsWaitPage,
    Results
]