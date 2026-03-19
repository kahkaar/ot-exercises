import unittest

from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_card_balance_is_correct_string(self):
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.00 euroa")

    def test_card_balance_is_correct(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_card_balance_is_correct_after_loading_money(self):
        self.maksukortti.lataa_rahaa(250)
        self.assertEqual(self.maksukortti.saldo_euroina(), 12.5)

    def test_card_balance_is_correct_after_taking_money(self):
        self.maksukortti.ota_rahaa(250)
        self.assertEqual(self.maksukortti.saldo_euroina(), 7.5)

    def test_card_balance_is_correct_after_taking_too_much_money(self):
        self.maksukortti.ota_rahaa(1250)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_ota_rahaa_returns_true_if_enough_money(self):
        self.assertEqual(self.maksukortti.ota_rahaa(250), True)

    def test_ota_rahaa_returns_false_if_not_enough_money(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1250), False)
