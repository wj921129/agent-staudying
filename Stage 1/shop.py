class User:
    def __init__(self, name):
        self.name = name

    def userInfo(self):
        return f'姓名：{self.name}'

class ATM:
    user_balance = {"李磊": 1000, "阿刁": 2000}

    def __init__(self, user):
        self.user = user
        self.balance = self.user_balance[self.user.name]

    def getBalance(self):
        print(f'{self.user.name}的余额为{self.balance}元')
        return self.balance

    def saveMoney(self, money):
        self.balance += money
        print(f'{self.user.name}已存款{money}元，当前余额为{self.balance}元')

    def fetchMoney(self, money):
        self.balance -= money
        print(f'{self.user.name}已取款{money}元，当前余额为{self.balance}元')
