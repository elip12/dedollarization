from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Description of the game: How to play and returns expected
class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Trade(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['trade_attempted']

    def vars_for_template(self):
        # self.session.vars['pairs'] is a list of rounds.
        # each round is a dict of (group,id):(group,id) pairs.
        group_id = 0 if self.participant.vars['group_color'] == Constants.red else 1

        # gets a another pair
        # the other pair is the pair that is paired with the current player
        other_group, other_id = self.session.vars['pairs'][self.round_number - 1][
            (group_id, self.player.id_in_group - 1)]
        other_player = self.subsession.get_groups()[other_group].get_player_by_id(other_id + 1)

        # whatever color token they were assigned in models.py
        self.player.token_color = self.player.participant.vars['token']
        self.player.other_token_color = other_player.participant.vars['token']

        # defining roles as in models.py
        # ensuring opposites, such that half are producers and half are consumers
        self.player.role_pre = 'Consumer' if self.player.participant.vars['token'] != Constants.trade_good else 'Producer'
        self.player.other_role_pre = 'Consumer' if self.player.other_token_color != Constants.trade_good else 'Producer'

        # defining group color as in models.py
        self.player.group_color = self.player.participant.vars['group_color']
        self.player.other_group_color = other_player.participant.vars['group_color']

        if False: #treatment = 'bots': # or whatever
            other_player.trade() 
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
        # similar to above in Trade()
        group_id = 0 if self.player.participant.vars['group_color'] == Constants.red else 1 
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
            # only 1 player actually switches the goods
            if not self.player.trade_succeeded:
                # switch tokens
                self.player.participant.vars['token'] = self.player.other_token_color
                other_player.participant.vars['token'] = self.player.token_color
                # set players' trade_succeeded field
                self.player.trade_succeeded = True
                other_player.trade_succeeded = True
            # give the consumer a payoff
            if self.player.role_pre == 'Consumer':
                round_payoff = Constants.reward
        else:
            self.player.trade_succeeded = False

        # penalties for self
        # if your token matches your group color
        if self.player.participant.vars['token'] == self.participant.vars['group_color']:
            round_payoff -= c(self.session.config['token_store_cost_homogeneous'])

        # if you don't have a token?
        elif self.player.participant.vars['token'] != Constants.trade_good:
            round_payoff -= c(self.session.config['token_store_cost_heterogeneous'])

        # set payoffs
        self.player.set_payoffs(round_payoff)
        if self.player.trade_succeeded:
            new_token_color = self.player.other_token_color
        else:
            new_token_color = self.player.token_color
        # tell bot to compute its own trade
        if False: #treatment = 'bots': # or whatever
            other_player.compute_results()
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
    

class PostResultsWaitPage(WaitPage):
    body_text = 'Waiting for other participants to finish viewing results.'
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        pass

page_sequence = [
    Introduction,
    Trade,
    ResultsWaitPage,
    Results,
    PostResultsWaitPage,
]

