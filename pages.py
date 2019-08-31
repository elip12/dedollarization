from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Trade(Page):
    form_model = 'player'
    form_fields = [
        'role_pre',
        'trade_attempted',
    ]

    def vars_for_template(self):
    '''
        session.vars['pairs'] is a list of rounds.
        each round is a dict of (group,id):(group,id) pairs.
    '''
        group_id = 0 if self.participant.vars['group_color'] == 'Red' else 1 
        other_group, other_id = session.vars['pairs'][self.round_number][
            (group_id, self.player.id_in_group)]
        other_player = self.get_groups()[other_group].get_player_by_id(other_id)
        other_token = other_player.partipant.vars['token']
        other_group_color = other_player.participant.vars['group_color']

        return {
            'token_color': self.player.participant.vars['token'],
            'group_color': self.player.participant.vars['group_color'],
            'other_role_pre': other_role_pre,
            'other_token_color': other_token,
            'other_group_color': other_group_color,
        {

class ResultsWaitPage(WaitPage):
    form_model = 'player'
    form_fields = [
        'role_post',
        'token_color',
        'trade_succeeded',
        'group_color',
        'round_payoff',
    ]
    
    def vars_for_template(self):
        group_id = 0 if self.participant.vars['group_color'] == 'Red' else 1 
        other_group, other_id = session.vars['pairs'][self.round_number][
            (group_id, self.player.id_in_group)]
        other_player = self.get_groups()[other_group].get_player_by_id(other_id)
        other_token = other_player.partipant.vars['token']
        other_group_color = other_player.participant.vars['group_color']
        
        ''' handle the logic for switching tokens here '''

        return {
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
        {


page_sequence = [
    Trade,
    ResultsWaitPage,
    Results
]
