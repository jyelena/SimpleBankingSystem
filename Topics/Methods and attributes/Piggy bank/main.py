class PiggyBank:
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents

    def add_money(self, deposit_dollars, deposit_cents):
        self.cents += deposit_cents
        self.dollars += self.cents // 100 + deposit_dollars
        self.cents = self.cents % 100
