

class Card():
    """Class for Card"""
    def __init__(self, suit, value=None):
        self.suit = suit
        self.value = value
    
    def clone(self, value):
        return Card(self.suit, value)

class Deck():
    """Class for Deck"""

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
        self.build_cards("Copas")
        self.build_cards("Ouros")
        self.build_cards("Espadas")
        self.build_cards("Paus")
    
    def build_cards(self, suit):
        suit_card = Card(suit)
        self.cards.append(suit_card.clone("A"))
        self.cards.append(suit_card.clone("J"))
        self.cards.append(suit_card.clone("Q"))
        self.cards.append(suit_card.clone("K"))
        for number in range(2,8): 
            value = str(number)
            card = suit_card.clone(value)
            self.cards.append(card)


class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        

if __name__ == '__main__':
  # cardCopas = Card("Copas")
  # card = cardCopas.clone("2")
  # print "Card 1"
  # print card.suit
  # print card.value
  # card2 = cardCopas.clone("3")
  # print "Card 2"
  # print card2.suit
  # print card2.value
  deck = Deck.get_instance()
  for card in deck.cards:
    print card.suit + " " + card.value