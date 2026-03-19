import unittest

from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_created_kassapaate_exists(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_initial_balance_amount_is_100000(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_initial_edulliset_amount_is_0(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_initial_maukkaat_amount_is_0(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_returns_correctly(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)

    def test_syo_edullisesti_kateisella_increases_kassassa_rahaa(self):
        self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_syo_maukkaasti_kateisella_returns_correctly(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_syo_maukkaasti_kateisella_increases_kassassa_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)

    def test_edulliset_amount_increases_after_syo_edullisesti_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukkaat_amount_increases_after_syo_maukkaasti_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_returns_false_if_not_enough_money_for_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

    def test_returns_false_if_not_enough_money_for_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)

    def test_kassassa_rahaa_does_not_increase_if_not_enough_money_for_edullinen(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_kassassa_rahaa_does_not_increase_if_not_enough_money_for_maukas(self):
        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_edulliset_amount_does_not_increase_if_not_enough_money(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaat_amount_does_not_increase_if_not_enough_money(self):
        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_card_payment_for_edullinen_returns_true_if_enough_money(self):
        self.assertEqual(
            self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)

    def test_card_payment_for_maukas_returns_true_if_enough_money(self):
        self.assertEqual(
            self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)

    def test_card_payment_for_edullinen_decreases_card_balance(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 760)

    def test_card_payment_for_maukas_decreases_card_balance(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 600)

    def test_card_payment_does_not_increase_edulliset_if_not_enough_money(self):
        kortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_card_payment_does_not_increase_maukkaat_if_not_enough_money(self):
        kortti = Maksukortti(300)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_card_payment_for_edullinen_returns_false_if_not_enough_money(self):
        kortti = Maksukortti(200)
        self.assertEqual(
            self.kassapaate.syo_edullisesti_kortilla(kortti), False)

    def test_card_payment_for_maukas_returns_false_if_not_enough_money(self):
        kortti = Maksukortti(300)
        self.assertEqual(
            self.kassapaate.syo_maukkaasti_kortilla(kortti), False)

    def test_card_payment_does_not_increase_kassassa_rahaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_lataa_rahaa_kortille_increases_card_balance(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)

    def test_lataa_rahaa_kortille_increases_kassassa_rahaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005)

    def test_lataa_rahaa_kortille_does_not_increase_kassassa_rahaa_if_amount_is_negative(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
