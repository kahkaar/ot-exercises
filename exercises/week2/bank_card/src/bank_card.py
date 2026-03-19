AFFORDABLE = 250
LUXURY = 400


class BankCard():
    def __init__(self, balance: int):
        self.balance = balance

    def eat_affordably(self):
        if self.balance >= AFFORDABLE:
            self.balance -= AFFORDABLE

    def eat_luxuriously(self):
        if self.balance >= LUXURY:
            self.balance -= LUXURY

    def load_money(self, amount: int):
        if amount < 0:
            return

        self.balance += amount

        if self.balance > 15000:
            self.balance = 15000

    def balance_in_euros(self):
        return self.balance / 100

    def __str__(self):
        balance_euros = round(self.balance / 100, 2)
        return "The card has {:0.2f} euros".format(balance_euros)
