from maksukortti import Maksukortti

AFFORDABLE = 240
EXPENSIVE = 400


class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def _add_money_to_register(self, amount: int):
        self.kassassa_rahaa += amount

    def syo_edullisesti_kateisella(self, amount: int):
        if amount < AFFORDABLE:
            return amount

        self._add_money_to_register(AFFORDABLE)
        self.edulliset += 1
        return amount - AFFORDABLE

    def syo_maukkaasti_kateisella(self, amount: int):
        if amount < EXPENSIVE:
            return amount

        self._add_money_to_register(EXPENSIVE)
        self.maukkaat += 1
        return amount - EXPENSIVE

    def syo_edullisesti_kortilla(self, card: Maksukortti):
        if card.saldo < AFFORDABLE:
            return False

        card.ota_rahaa(AFFORDABLE)
        self.edulliset += 1
        return True

    def syo_maukkaasti_kortilla(self, card: Maksukortti):
        if card.saldo < EXPENSIVE:
            return False

        card.ota_rahaa(EXPENSIVE)
        self.maukkaat += 1
        return True

    def lataa_rahaa_kortille(self, card: Maksukortti, amount: int):
        if amount < 0:
            return

        card.lataa_rahaa(amount)
        self.kassassa_rahaa += amount

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100
