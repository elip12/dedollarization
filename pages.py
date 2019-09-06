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
    form_fields = ['trade_attempted']

    def vars_for_template(self):
        # self.session.vars['pairs'] is a list of rounds.
        # each round is a dict of (group,id):(group,id) pairs.
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1 
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        
        self.player.token_color = self.player.participant.vars['token']
        self.player.other_token_color = other_player.participant.vars['token']
        self.player.role_pre = 'Consumer' if self.player.participant.vars['token'] != Constants.trade_good else 'Producer'
        self.player.other_role_pre = 'Consumer' if self.player.other_token_color != Constants.trade_good else 'Producer'
        self.player.group_color = self.player.participant.vars['group_color']
        self.player.other_group_color = other_player.participant.vars['group_color']
        
        return {
            'role_pre': self.player.role_pre,
            'other_role_pre': self.player.other_role_pre,
            'token_color': self.player.participant.vars['token'],
            'group_color': self.player.participant.vars['group_color'],
            'other_token_color': self.player.other_token_color,
            'other_group_color': self.player.other_group_color,
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
        # identify trading partner
        group_id = 0 if self.player.participant.vars['group_color'] == Constants.red else 1 
        print(group_id, self.player.id_in_group)
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        # get other player object
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)
        # define initial round payoffs
        round_payoff = c(0)
        other_round_payoff = c(0)
        # logic for switching objects on trade
        # if both players attempted a trade, it must be true
        # that one is a producer and one is a consumer.
        # Only 1 player performs the switch
        if self.player.trade_attempted and other_player.trade_attempted: 
            # set players' trade_succeeded field
            self.player.trade_succeeded = True
            # give the consumer a payoff
            if self.player.role_pre == 'Consumer':
                round_payoff = Constants.reward
            # only 1 player actually switches the goods
            if group_id < other_group or (group_id == other_group \
            and self.player.id_in_group < other_id):
                # switch tokens
                self.player.participant.vars['token'] = self.player.other_token_color
                other_player.participant.vars['token'] = self.player.token_color
        else:
            self.player.trade_succeeded = False
        # penalties for self
        if self.player.participant.vars['token'] == self.participant.vars['group_color']:
            round_payoff -= c(self.session.config['token_store_cost_homogeneous'])
        elif self.player.participant.vars['token'] != Constants.trade_good:
            round_payoff -= c(self.session.config['token_store_cost_heterogeneous'])
        # set payoffs
        self.player.set_payoffs(round_payoff)

        # TODO: change return dict to use new var names, make red, blue, none into constants. red, blue, trade_good or something, identify why thing was subtracting 2 0sometimes.
        if self.player.trade_succeeded and self.player.role_pre == 'Consumer':
            new_token_color = self.player.other_token_color
        else:
            new_token_color = Constants.trade_good
        return {
            'token_color': self.player.token_color,
            'role_pre': self.player.role_pre,
            'other_role_pre': self.player.other_role_pre,
            'trade_attempted': self.player.trade_attempted,
            'group_color': self.player.group_color,
            'trade_succeeded': self.player.trade_succeeded,
            'new_token_color': new_token_color,
            'round_payoff': self.player.payoff,
        }

page_sequence = [
    Introduction,
    Trade,
    ResultsWaitPage,
    Results
]

