from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from .automated_trader import AutomatedTrader

class Constants(BaseConstants):
    name_in_url = 'producer_consumer'
    players_per_group = 4
    num_rounds = 1
    endowment = c(50)
    reward = c(20)
    red = 'Red'
    blue = 'Blue'
    trade_good = 'Trade Good'

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:

            # puts players into groups of size players_per_group
            self.group_randomly()
            n_groups = len(self.get_groups()) * 2

            # create random pairings
            # for the whole session
            # a way to pair people given certain probabilities of
            # getting paired within your group or within the other group
            self.session.vars['pairs'] = []
            for r in range(Constants.num_rounds):
                # maps traders to their trading partners
                # (group_id, player_id) <=> (group_id, player_id)
                # so that a player can look up who their trading partner is
                # in this map
                pairs = {}
                groups = []
                for gi in range(n_groups):
                    # create player ids in group
                    # ex: 1,2,3,4
                    g = [i for i in range(Constants.players_per_group)]
                    
                    # shuffle player numbers
                    # ex: 1,3,2,4
                    random.shuffle(g)

                    # NOTE: self.session.config['probability_of_same_group'] times
                    # Constants.players_per_group needs to cleanly divide 2.
                    index = int(Constants.players_per_group *
                        self.session.config['probability_of_same_group'])
                    assert(index % 2 == 0)

                    # sampling probability_of_same_group % of players from g
                    # ex: 1,3
                    g_sample_homogeneous = g[:index]
                    
                    # sampling other 1 - probability_of_same_group % of players from g
                    # ex: 2,4
                    g_sample_heterogeneous = g[index:]
                    # pairing homogeneous
                    # ex: (0,1) <=> (0,3)
                    #     (0,3) <=> (0,1)
                    for i in range(0, index, 2):
                        pairs[(gi, g_sample_homogeneous[i])] = (gi, g_sample_homogeneous[i + 1])
                        pairs[(gi, g_sample_homogeneous[i + 1])] = (gi, g_sample_homogeneous[i])
                    # store the heterogeneous players so they can be paired later
                    groups.append(g_sample_heterogeneous)
   
                # pair traders between groups
                # flatten into list of pairs.
                # ex: [[1,2,3], [4,2,1], [3,2,4], [4,1,3]]
                # => [(0,1), (0,2), (0,3), (1,4), (1,2), (1,1) ...]
                g = [(i, p) for i in range(n_groups) for p in groups[i]]
                # num groups needs to be even (b/c one bot group per player group)
                # therefore len(g) is even
                random.shuffle(g)
                # ex: (0,4) <=> (1,8)
                #     (1,8) <=> (0,4)
                for i in range(0, len(g), 2):
                    pairs[g[i]] = g[i + 1]
                    pairs[g[i + 1]] = g[i]

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

            # BOTS
            self.session.vars['automated_traders'] = {}
            # automated traders are always in 2nd half of groups
            for gi in range(n_groups // 2, n_groups):
                group_color = Constants.blue
                roles = [Constants.trade_good for n in range(Constants.players_per_group // 2)]
                roles += [group_color for n in range(Constants.players_per_group // 2)]
                random.shuffle(roles)
                
                # within the pair, find group number and position in group
                for pi in range(Constants.players_per_group):
                    trader = AutomatedTrader(self.session, pi + 1)
                    trader.participant.vars['group_color'] = group_color
                    trader.participant.vars['group'] = gi
                    trader.participant.payoff += Constants.endowment
                    trader.participant.vars['token'] = roles[pi]
                    self.session.vars['automated_traders'][(gi, pi)] = trader

            # player groups
            for g_index, g in enumerate(self.get_groups()):
                group_color = Constants.red

                # define random roles for players (producer/consumer),
                # ensuring half are producers and half are consumers
                # denotes half with a trade good
                # denotes half with group color
                roles = [Constants.trade_good for n in range(Constants.players_per_group // 2)]
                roles += [group_color for n in range(Constants.players_per_group // 2)]
                random.shuffle(roles)

                # set each player's group color, and starting token (which
                # determines who is going to be a producer vs consumer
                # whatever number (p_index) the player is defines role
                for p_index, p in enumerate(g.get_players()):
                    p.participant.vars['group_color'] = group_color
                    p.participant.vars['group'] = g_index
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

