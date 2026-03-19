import unittest

from bank_card import BankCard


class TestBankCard(unittest.TestCase):
    def setUp(self):
        self.card = BankCard(1000)

    def test_constructor_sets_balance_correctly(self):
        self.assertEqual(str(self.card), "The card has 10.00 euros")

    def test_eat_affordably_reduces_balance_correctly(self):
        self.card.eat_affordably()
        self.assertEqual(self.card.balance_in_euros(), 7.5)

    def test_eat_luxuriously_reduces_balance_correctly(self):
        self.card.eat_luxuriously()
        self.assertEqual(self.card.balance_in_euros(), 6.0)

    def test_eat_affordably_does_not_reduce_balance_below_zero(self):
        card = BankCard(200)
        card.eat_affordably()

        self.assertEqual(card.balance_in_euros(), 2.0)

    def test_eat_luxuriously_does_not_reduce_balance_below_zero(self):
        card = BankCard(300)
        card.eat_luxuriously()

        self.assertEqual(card.balance_in_euros(), 3.0)

    def test_load_money_increases_balance_correctly(self):
        self.card.load_money(2500)

        self.assertEqual(self.card.balance_in_euros(), 35.0)

    def test_load_money_does_not_go_over_maximum(self):
        self.card.load_money(20000)

        self.assertEqual(self.card.balance_in_euros(), 150.0)

    def test_load_money_does_not_accept_negative_amount(self):
        self.card.load_money(-500)

        self.assertEqual(self.card.balance_in_euros(), 10.0)
