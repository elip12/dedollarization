from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Description of the game: How to play and returns expected
class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Trade(Page):
    timeout_seconds = 30
    form_model = 'player'
    form_fields = [
        'trade_attempted',
    ]

    def vars_for_template(self):
        # self.session.vars['pairs'] is a list of rounds.
        # each round is a dict of (group,id):(group,id) pairs.
        group_id = 0 if self.participant.vars['group_color'] == 'Red' else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        other_token = other_player.participant.vars['token']
        other_group_color = other_player.participant.vars['group_color']
        role_pre = 'Consumer' if self.player.participant.vars['token'] != 'None' else 'Producer'
        other_role_pre = 'Consumer' if other_token != 'None' else 'Producer'
        self.player.role_pre = role_pre
        self.player.other_role_pre = other_role_pre
        self.player.group_color = self.player.participant.vars['group_color']
        self.player.other_group_color = other_group_color
        return {
            'role_pre': role_pre,
            'other_role_pre': other_role_pre,
            'token_color': self.player.participant.vars['token'],
            'group_color': self.player.participant.vars['group_color'],
            'other_token_color': other_token,
            'other_group_color': other_group_color,
        }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.trade_attempted = False

class ResultsWaitPage(WaitPage):
    body_text = 'Waiting for other participants to decide.'
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        pass

class Results(Page):
    timeout_seconds = 30
    
    def vars_for_template(self):
        group_id = 0 if self.player.participant.vars['group_color'] == 'Red' else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        other_token = other_player.participant.vars['token']
        other_group_color = other_player.participant.vars['group_color']
        round_payoff = c(0)
        # switching tokens
        initial_token_color = self.player.participant.vars['token']
        if self.player.trade_attempted and other_player.trade_attempted \
            and not other_player.trade_succeeded: # to avoid switching back again    
            self.player.participant.vars['token'] = other_token
            other_player.participant.vars['token'] = initial_token_color
            trade_succeeded = True
            if initial_token_color != 'None':
                round_payoff = c(20)
        else:
            trade_succeeded = False
        new_token_color = self.player.participant.vars['token']
        if initial_token_color != 'None':
            role_pre = 'Consumer'
        else:
            role_pre = 'Producer'
        if other_token != 'None':
            other_role_pre = 'Consumer'
        else:
            other_role_pre = 'Producer'
        token_color = initial_token_color if initial_token_color != 'None' \
            else new_token_color
        # penalties
        if self.participant.vars['group_color'] == new_token_color:
            round_payoff -= c(self.session.config['token_store_cost_homogeneous'])
        elif token_color != 'None':
            round_payoff -= c(self.session.config['token_store_cost_heterogeneous'])
        self.player.set_payoffs(round_payoff)
        self.player.token_color = token_color
        self.player.trade_succeeded = trade_succeeded
        return {
            'token_color': token_color,
            'role_pre': role_pre,
            'other_role_pre': other_role_pre,
            'trade_attempted': self.player.trade_attempted,
            'initial_token_color': initial_token_color,
            'group_color': self.player.participant.vars['group_color'],
            'trade_succeeded': trade_succeeded,
            'new_token_color': new_token_color,
            'round_payoff': round_payoff,
        }


page_sequence = [
    Introduction,
    Trade,
    ResultsWaitPage,
    Results
]

