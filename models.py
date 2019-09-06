from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'producer_consumer'
    players_per_group = 8
    num_rounds = 2
    endowment = c(50)
    reward = c(20)
    red = 'Red'
    blue = 'Blue'
    trade_good = 'Trade Good'

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()

            # create random pairings
            self.session.vars['pairs'] = []
            for r in range(Constants.num_rounds):
                pairs = {}

                # a way to pair people given certain probabilities of
                # getting paired within your group or within the other group
                # NOTE: self.session.config['probability_of_same_group'] times
                # Constants.players_per_group needs to be an integer.
                g1 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g1)
                g1_sample_homogeneous = random.sample(g1,
                    int(Constants.players_per_group
                    * self.session.config['probability_of_same_group']))
                g1_sample_heterogeneous = [x for x in g1
                    if x not in g1_sample_homogeneous]
                g2 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g2)
                g2_sample_homogeneous = random.sample(g2,
                    int(Constants.players_per_group
                    * self.session.config['probability_of_same_group']))
                g2_sample_heterogeneous = [x for x in g2
                    if x not in g2_sample_homogeneous]
                for i in range(0, len(g1_sample_homogeneous), 2):
                    pairs[(0, g1_sample_homogeneous[i])] = (0,
                        g1_sample_homogeneous[i + 1])
                    pairs[(0, g1_sample_homogeneous[i + 1])] = (0,
                        g1_sample_homogeneous[i])
                for i in range(0, len(g2_sample_homogeneous), 2):
                    pairs[(1, g2_sample_homogeneous[i])] = (1,
                        g2_sample_homogeneous[i + 1])
                    pairs[(1, g2_sample_homogeneous[i + 1])] = (1,
                        g2_sample_homogeneous[i])
                for i in range(len(g1_sample_heterogeneous)):
                    pairs[(0, g1_sample_heterogeneous[i])] = (1,
                        g2_sample_heterogeneous[i])
                    pairs[(1, g2_sample_heterogeneous[i])] = (0,
                        g1_sample_heterogeneous[i])
                self.session.vars['pairs'].append(pairs)
                    
            # there will always only be 2 groups
            for g_index, g in enumerate(self.get_groups()):
                # set group color for player
                group_color = Constants.red if g_index == 0 else Constants.blue
                # define random roles for players (producer/consumer),
                # ensuring half are producers and half are consumers
                roles = [Constants.trade_good for n in range(int(Constants.players_per_group / 2))]
                roles += [group_color for n in range(
                    int(Constants.players_per_group / 2))]
                random.shuffle(roles)
                # set each player's group color, and starting token (which
                # defines role
                for p_index, p in enumerate(g.get_players()):
                    p.participant.vars['group_color'] = group_color
                    p.participant.vars['token'] = roles[p_index]
                    p.participant.payoff += Constants.endowment
        else:
            self.group_like_round(1)
            
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    role_pre = models.StringField() # 'Producer', 'Consumer'
    other_role_pre = models.StringField()
    token_color = models.StringField() # Constants.red, Constants.blue, None
    other_token_color = models.StringField()
    group_color = models.StringField() # Constants.red, Constants.blue
    other_group_color = models.StringField()
    trade_attempted = models.BooleanField(
        choices=[
            [False, 'No'],
            [True, 'Yes'],
        ]
    )
    trade_succeeded = models.BooleanField()

    def set_payoffs(self, round_payoff):
        self.payoff = round_payoff

