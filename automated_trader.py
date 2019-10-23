class Participant():
    def __init__(self):
        self.vars = {}

class Round():
    def __init__(self):
        self.role_pre = None
        self.other_role_pre = None
        self.token_color = None
        self.other_token_color = None
        self.group_color = None
        self.other_group_color = None
        self.trade_attempted = None
        self.trade_succeeded = None

    def over(self):
        if all(vars(self).values()):
            return True
        return False
    
class AutomatedTrader():
    def __init__(self):
        self.participant = Participant()
        self.__round_data = [Round()]

    def __check_round_over(self):
        r = self.__round_data[-1]
        if r.over():
            self.round_data.append(Round())
    
    def in_round(self, n):
        return self.__round_data[n - 1]
    
    @property
    def role_pre(self):
        r = self.__round_data[-1]
        return r.role_pre

    @role_pre.setter
    def role_pre(self, v):
        self.__check_round_over()
        self.__round_data[-1].role_pre = v

    @property
    def other_role_pre(self):
        r = self.__round_data[-1]
        return r.other_role_pre

    @other_role_pre.setter
    def other_role_pre(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_role_pre = v
    
    @property
    def token_color(self):
        r = self.__round_data[-1]
        return r.token_color

    @token_color.setter
    def token_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].token_color = v

    @property
    def other_token_color(self):
        r = self.__round_data[-1]
        return r.other_token_color

    @other_token_color.setter
    def other_token_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_token_color = v

    @property
    def group_color(self):
        r = self.__round_data[-1]
        return r.group_color

    @group_color.setter
    def group_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].group_color = v

    @property
    def other_group_color(self):
        r = self.__round_data[-1]
        return r.other_group_color

    @other_group_color.setter
    def other_group_color(self, v):
        self.__check_round_over()
        self.__round_data[-1].other_group_color = v

    @property
    def trade_attempted(self):
        r = self.__round_data[-1]
        return r.trade_attempted

    @trade_attempted.setter
    def trade_attempted(self, v):
        self.__check_round_over()
        self.__round_data[-1].trade_attempted = v

    @property
    def trade_succeeded(self):
        r = self.__round_data[-1]
        return r.trade_succeeded

    @trade_succeeded.setter
    def trade_succeeded(self, v):
        self.__check_round_over()
        self.__round_data[-1].trade_succeeded = v

