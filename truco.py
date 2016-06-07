import random

class Card():
    """Prototype class for Card"""
    def __init__(self, suit, value=None):
        self.suit = suit
        self.value = value
    
    def clone(self, value):
        return Card(self.suit, value)

    def __str__(self):
        suit = self.suit
        value = self.value
        if value is "A":
            value = "As"
        elif value is "K":
            value = "Rei"
        elif value is "Q":
            value = "Dama"
        elif value is "J":
            value = "Valete"

        return value + " de " + suit

class Deck():
    """Singleton Pool class for Deck"""

    CARDS_QUANTITY = 40
    instance = None
    
    @staticmethod
    def get_instance():
        if Deck.instance is None:
            Deck.instance = Deck()
        return Deck.instance

    def __init__(self):
        self.cards = []
        self.__init_deck()

    def __init_deck(self):
        self.__create_cards("Copas")
        self.__create_cards("Ouros")
        self.__create_cards("Espadas")
        self.__create_cards("Paus")
    
    def __create_cards(self, suit):
        suit_card = Card(suit)
        self.cards.append(suit_card.clone("A"))
        self.cards.append(suit_card.clone("J"))
        self.cards.append(suit_card.clone("Q"))
        self.cards.append(suit_card.clone("K"))
        for number in range(2,8): 
            value = str(number)
            card = suit_card.clone(value)
            self.cards.append(card)

    def shuffle(self):
        self.__check_deck()
        random.shuffle(self.cards)

    def __check_deck(self):
        """ Check deck integrity """
        if len(self.cards) is not self.CARDS_QUANTITY:
            raise Exception("Alguem esta roubando e nao devolveu todas as cartas!")

    def get_top_card(self):
        top_card = self.cards[0]
        # Remove it from pool
        self.cards.remove(top_card)
        return top_card

    def get_bottom_card(self):
        bottom_card = self.cards[len(self.cards) - 1]
        # Remove it from pool
        self.cards.remove(bottom_card)
        return bottom_card

    def keep_card(self, card):
        # Add the card back to the pool
        self.cards.append(card)


if __name__ == '__main__':
    deck = Deck.get_instance()
    try:
        deck.shuffle()
    except Exception, e:
        print e
    card = deck.get_bottom_card()
    print card
    deck.keep_card(card)
    try:
        deck.shuffle()
    except Exception, e:
        print e