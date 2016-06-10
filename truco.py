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
        for number in range(2, 8):
            value = str(number)
            card = suit_card.clone(value)
            self.cards.append(card)

    def shuffle(self):
        self.__check_deck()
        random.shuffle(self.cards)

    def __check_deck(self):
        """ Check deck integrity """
        if len(self.cards) is not self.CARDS_QUANTITY:
            raise Exception("""Alguem esta roubando e nao
                             devolveu todas as cartas!""")

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


class Hand(object):
    """ Represents the player hand """

    def __init__(self, cards):
        self.cards = cards

    def throw_card(self, card_position=0):

        if card_position in range(1, len(self.cards) + 1):
            card_position -= 1
            card =  self.cards[card_position] 
            self.__remove_card(card)
        else:
            # Return the first card of the hand by default
            if not self.cards:
                raise Exception("Mao vazia")
            else:
                card = self.cards[0]
                self.__remove_card(card)

        return card

    def __remove_card(self, card):
        self.cards.remove(card)

    def __str__(self):
        cards_str = ""
        for card in self.cards:
            cards_str += str(card) + ", "
        return cards_str

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

    print
    cards = []
    for i in range(1, 4):
        cards.append(deck.get_bottom_card())

    hand = Hand(cards)
    print hand

    # Throwing first card
    hand.throw_card()
    print hand

    # Throwing third card
    hand.throw_card()
    print hand

    # Throwing second card
    hand.throw_card()
    print hand

    try:
        print hand.throw_card()
        print hand
    except Exception, e:
        print e

class CardCheck:

    def get_winner(self):
        pass

class Round:

    def __init__(self, match):
        self.match = match
        self.round_cards = {}

    def add_round_card(self, player, card):
        self.round_cards[player] = card

    def end_round(self):
        self.card_checker = CardCheck(self.round_cards)
        winner = self.card_checker.get_winner()
        return winner


class Match:
    
    def __init__(self, game):
        self.game = game
        self.current_round = Round(self)
        self.rounds = []

    def receive_card(self, player, card):
        self.current_round.add_round_card(player, card)

    def end_current_round(self):
        winner = self.current_round.end_round()
        rounds.append(self.current_round)
        self.current_round = Round(self)

