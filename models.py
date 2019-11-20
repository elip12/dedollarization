from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from .automated_trader import AutomatedTrader

class Constants(BaseConstants):
    name_in_url = 'producer_consumer'
    players_per_group = 4
    auto_traders_per_group = 4
    num_rounds = 1
    endowment = c(50)
    reward = c(20)
    red = 'Red'
    blue = 'Blue'
    trade_good = 'Trade Good'

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:

            # puts into two groups
            self.group_randomly()

            # create random pairings
            # for the whole session
            self.session.vars['pairs'] = []
            for r in range(Constants.num_rounds):

                # holds tuples
                pairs = {}

                tuples = []

                # a way to pair people given certain probabilities of
                # getting paired within your group or within the other group

                # NOTE: self.session.config['probability_of_same_group'] times
                # Constants.players_per_group needs to be an integer.

                # shuffle player numbers
                # ex: 1,2,3,4
                g1 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g1)

                # sampling half from g1
                # ex: 1,3
                g1_sample_homogeneous = random.sample(g1, int(Constants.players_per_group * self.session.config['probability_of_same_group']))
                # other half
                # ex: 2,4
                g1_sample_heterogeneous = [x for x in g1 if x not in g1_sample_homogeneous]

                # shuffle player numbers
                #  ex: 5,6,7,8
                g2 = [i for i in range(Constants.players_per_group)]
                random.shuffle(g2)

                # sampling half from g2
                # ex: 5,7
                g2_sample_homogeneous = random.sample(g2, int(Constants.players_per_group * self.session.config['probability_of_same_group']))
                # other half
                # ex: 6,8
                g2_sample_heterogeneous = [x for x in g2 if x not in g2_sample_homogeneous]

                # pairing
                # only g1 homogeneous
                # ex: (0,1) <=> (0,3)
                #     (0,3) <=> (0,1)
                for i in range(0, len(g1_sample_homogeneous), 2):
                    pairs[(0, g1_sample_homogeneous[i])] = (0, g1_sample_homogeneous[i + 1])
                    pairs[(0, g1_sample_homogeneous[i + 1])] = (0, g1_sample_homogeneous[i])

                # pairing
                # only g2 homogeneous
                # ex: (1,5) <=> (1,7)
                #     (1,7) <=> (1,5)
                for i in range(0, len(g2_sample_homogeneous), 2):
                    pairs[(1, g2_sample_homogeneous[i])] = (1, g2_sample_homogeneous[i + 1])
                    pairs[(1, g2_sample_homogeneous[i + 1])] = (1, g2_sample_homogeneous[i])

                # pairing
                # both g1 and g2 heterogeneous
                # ex: (0,2) <=> (1,6)
                #     (1,6) <=> (0,2)

                # ex: (0,4) <=> (1,8)
                #     (1,8) <=> (0,4)
                for i in range(len(g1_sample_heterogeneous)):
                    pairs[(0, g1_sample_heterogeneous[i])] = (1, g2_sample_heterogeneous[i])
                    pairs[(1, g2_sample_heterogeneous[i])] = (0, g1_sample_heterogeneous[i])

                # SAME PROCESS FOR AUTOMATED_TRADERS

                g3 = [i for i in range(Constants.auto_traders_per_group)]
                random.shuffle(g3)
                g3_sample_homogeneous = random.sample(g3, int(Constants.players_per_group * self.session.config['probability_of_same_group']))
                g3_sample_heterogeneous = [x for x in g1 if x not in g1_sample_homogeneous]

                g4 = [i for i in range(Constants.auto_traders_per_group)]
                random.shuffle(g2)
                g4_sample_homogeneous = random.sample(g4, int(Constants.players_per_group * self.session.config['probability_of_same_group']))
                g4_sample_heterogeneous = [x for x in g2 if x not in g2_sample_homogeneous]

                for i in range(0, len(g3_sample_homogeneous), 2):
                    pairs[(3, g3_sample_homogeneous[i])] = (3, g3_sample_homogeneous[i + 1])
                    pairs[(3, g3_sample_homogeneous[i + 1])] = (3, g3_sample_homogeneous[i])

                for i in range(0, len(g4_sample_homogeneous), 2):
                    pairs[(4, g4_sample_homogeneous[i])] = (4, g4_sample_homogeneous[i + 1])
                    pairs[(4, g4_sample_homogeneous[i + 1])] = (4, g4_sample_homogeneous[i])

                for i in range(len(g3_sample_heterogeneous)):
                    pairs[(3, g3_sample_heterogeneous[i])] = (4, g4_sample_heterogeneous[i])
                    pairs[(4, g4_sample_heterogeneous[i])] = (3, g4_sample_heterogeneous[i])

                self.session.vars['pairs'].append(pairs)

            # if there is only 1 group, then we can do another loop after this
            # one and do the exact same shit, except instantiating bots
            # instead of getting players with p.

            # if there can be more than 1 group, we can easily just repeat the
            # loop some number of times for the number of bot groups. And,
            # we will also need to change the loop above to
            # do not just 0 and 1 for g index but other numbers, and also change
            # the method for getting your group index since looking at your
            # color will not suffice anymore.

            # TRADERS

            self.session.vars['automated_traders'] = []
            # gets general counting index and each pair
            for general_index, tuple in enumerate(pairs):
                # within the pair, find group number and position in group
                for group_number, group_id in enumerate(tuple):
                    # if it's a trader
                    if group_number == 3 or 4:
                        trader = AutomatedTrader(self, group_id)
                        trader.participant.vars['group_color'] = Constants.blue
                        # trader.participant.vars['token'] = roles[]
                        self.session.vars['automated_traders'].append(trader)

            # player groups
            for g_index, g in enumerate(self.get_groups()):

                # CHANGE: only one color for the actual players
                #   bots will be other color
                #   there are still two groups (0, x), (1, x)
                #   but each of these group's color is red
                group_color = Constants.red if g_index == 0 or 1 else Constants.blue

                # define random roles for players (producer/consumer),
                # ensuring half are producers and half are consumers
                # denotes half with a trade good
                # denotes half with group color
                roles = [Constants.trade_good for n in range(int(Constants.players_per_group / 2))]
                roles += [group_color for n in range(int(Constants.players_per_group / 2))]
                random.shuffle(roles)

                # set each player's group color, and starting token (which
                # determines who is going to be a producer vs consumer
                # whatever number (p_index) the player is defines role
                # CHANGE: only one color for the actual players
                #   bots will be other color
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

