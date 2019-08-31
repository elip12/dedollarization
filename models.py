from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


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

            # create random pairings
            self.session.vars['pairs'] = []
            for r in Constants.num_rounds:
                pairs = {}

                # a way to pair people given certain probabilities of
                # getting paired within your group or within the other group
                # NOTE: Constants.probability_of_same_group times
                # Constants.players_per_group needs to be an integer.
                g1 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g1)
                g1_sample_homogeneous = random.sample(g1,
                    Constants.players_per_group
                    * Constants.probability_of_same_group)
                g1_sample_heterogeneous = [x for x in g1
                    if x not in g1_sample_homogeneous]
                g2 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g2)
                g2_sample_homogeneous = random.sample(g2,
                    Constants.players_per_group
                    * Constants.probability_of_same_group)
                g2_sample_heterogeneous = [x for x in g2
                    if x not in g2_sample_homogeneous]
                for i in range(0, len(g1_sample_homogeneous), 2):
                    pairs[(1, g1_sample_homogeneous[i])] = (1,
                        g1_sample_homogeneous[i + 1])
                    pairs[(1, g1_sample_homogeneous[i + 1])] = (1,
                        g1_sample_homogeneous[i])
                for i in range(0, len(g2_sample_homogeneous), 2):
                    pairs[(2, g2_sample_homogeneous[i])] = (2,
                        g2_sample_homogeneous[i + 1])
                    pairs[(2, g2_sample_homogeneous[i + 1])] = (2,
                        g2_sample_homogeneous[i])
                for i in range(len(g1_sample_heterogeneous)):
                    pairs[(1, g1_sample_heterogeneous[i])] = (2,
                        g2_sample_heterogeneous[i])
                    pairs[(2, g2_sample_heterogeneous[i])] = (1,
                        g1_sample_heterogeneous[i])
                self.session.vars['pairs'].append(pairs)
                    
            # there will always only be 2 groups
            for g_index, g in enumerate(self.get_groups()):
                # set group color for player
                group_color = 'Red' if g_index == 0 else 'Blue'
                # define random roles for players (producer/consumer),
                # ensuring half are producers and half are consumers
                roles = [None for n in range(Constants.players_per_group / 2)]
                roles += [group_color for n in range(
                    Constants.players_per_group / 2)]
                random.shuffle(roles)
                # set each player's group color, and starting token (which
                # defines role
                for p_index, p in enumerate(g.get_players()):
                    p.participant.vars['group_color'] = group_color
                    p.participant.vars['token'] = roles[p_index]
        else:
            self.group_like_round(1)
            
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
