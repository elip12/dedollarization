from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'consumer_producer'
    players_per_group = 8
    num_rounds = 6
    endowment = c(50)
    probability_of_same_group = .5

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()

            # there will always only be 2 groups
            for g_index, g in enumerate(self.get_groups()):
                group_color = 'Red' if g_index == 0 else 'Blue'
                roles = [None for n in range(Constants.players_per_group / 2)]
                roles += [group_color for n in range(
                    Constants.players_per_group / 2)]
                roles.shuffle()
                for p_index, p in enumerate(g.get_players()):
                    p.participant.vars['group_color'] = group_color
                    p.participant.vars['token'] = roles[p_index]
                    if p.participant.vars['token']:
                        p.participant.vars['role'] = 'Consumer'
                    else:
                        p.participant.vars['role'] = 'Producer'

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    role_pre = models.StringField() # 'Producer', 'Consumer'
    token_color = models.StringField() # 'Red', 'Blue', None
    group_color = models.StringField() # 'Red', 'Blue'
    other_role_pre = models.StringField()
    other_token_color = models.StringField()
    other_group_color = models.StringField()
    trade_attempted = models.BooleanField()
    trade_succeeded = models.BooleanField()
    round_payoff = models.CurrencyField()

    def set_payoffs(self):
        self.participant.payoff += self.round_payoff
        # possible more here?
