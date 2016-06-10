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

class CardCheck(object):
    """ Check the cards to know the round winner"""
    
    SHACKLES = {'zap' : Card("Paus", "4"),
                'hearts' : Card("Copas", "7"),
                'diamonds' : Card("Ouros", "7"),
                'ace_of_spades' : Card("Espadas", "A")
                }

    CARDS_VALUES = {
                    '3': 10,
                    '2': 9,
                    'A': 8,
                    'K': 7,
                    'J': 6,
                    'Q': 5,
                    '7': 4,
                    '6': 3,
                    '5': 2,
                    '4': 1
                }            

    def __init__(self, round_cards):
        self.round_cards = round_cards
        self.winner_card = self.check_winner_round()
    
    def get_winner(self):
        return self.winner_card

    def check_winner_round(self):
        winners_pairs = []

        pair_one_winner = self.check_shackles(self.round_cards['pair_one'])
        winners_pairs.append(pair_one_winner)
        pair_two_winner = self.check_shackles(self.round_cards['pair_two'])
        winners_pairs.append(pair_two_winner)
        
        winner_card = self.check_shackles(winners_pairs)   
        return winner_card

    def check_shackles(self, cards):
        fst_card_is_shackle = self.check_if_is_shackle(cards[0]); 
        snd_card_is_shackle = self.check_if_is_shackle(cards[1]); 
        if(fst_card_is_shackle and snd_card_is_shackle):
            winner_card = self.get_shackle_winner(cards)
        
        elif(not snd_card_is_shackle and fst_card_is_shackle):
            winner_card = cards[0]; 
        
        elif(not fst_card_is_shackle and snd_card_is_shackle):
            winner_card = cards[1]; 
        
        else:
            winner_card = self.get_winner_without_shackles(cards)

        return winner_card

    def check_if_is_shackle(self, card):
        zap = card.value is self.SHACKLES['zap'].value and card.suit is self.SHACKLES['zap'].suit
        hearts = card.value is self.SHACKLES['hearts'].value and card.suit is self.SHACKLES['hearts'].suit
        diamonds = card.value is self.SHACKLES['diamonds'].value and card.suit is self.SHACKLES['diamonds'].suit
        ace_of_spades = card.value is self.SHACKLES['ace_of_spades'].value and card.suit is self.SHACKLES['ace_of_spades'].suit

        if(zap or hearts or diamonds or ace_of_spades):
            is_shackle = True
        else:
            is_shackle = False

        return is_shackle

    def get_winner_without_shackles(self, cards):
        first_card = cards[0].value  
        second_card = cards[1].value  
        if(self.CARDS_VALUES[first_card] > self.CARDS_VALUES[second_card]):
            winner_card = cards[0]
        else:
            winner_card = cards[1]

        return winner_card
    def get_shackle_winner(self, cards):

        first_card_shackle = self.get_shackle(cards[0])
        second_card_shackle = self.get_shackle(cards[1])
        print first_card_shackle
        print second_card_shackle
        if(first_card_shackle is "zap"):
            winner = cards[0]
        elif(second_card_shackle is "zap"):
            winner = cards[1]     
        elif(first_card_shackle is "hearts"):
            winner = cards[0]
        elif(second_card_shackle is "hearts"):
            winner = cards[1]
        elif(first_card_shackle is "diamonds"):
            winner = cards[0]
        else:
            winner = cards[1]

        return winner

    def get_shackle(self, card):
        
        zap = card.value is self.SHACKLES['zap'].value and card.suit is self.SHACKLES['zap'].suit
        hearts = card.value is self.SHACKLES['hearts'].value and card.suit is self.SHACKLES['hearts'].suit
        diamonds = card.value is self.SHACKLES['diamonds'].value and card.suit is self.SHACKLES['diamonds'].suit
        ace_of_spades = card.value is self.SHACKLES['ace_of_spades'].value and card.suit is self.SHACKLES['ace_of_spades'].suit

        if(zap):
            shackle = "zap"
        elif(hearts):
            shackle = "hearts"
        elif(diamonds):
            shackle = "diamonds"
        else:
            shackle = "ace_of_spades"

        return shackle


class Player(object):
    """ Represents the player """

    def __init__(self, player_name, hand, game):
        self.player_name = player_name
        self.hand = hand
        self.game = game

    
class Pair(object):
    """ Represents the pair """

    def __init__(self, id_pair, players):
        self.id_pair = id_pair
        self.players = players

    players = {}.fromkeys(['player1','player2'],'player')


if __name__ == '__main__':
    deck = Deck.get_instance()
    try:
        deck.shuffle()
    except Exception, e:
        print e
    card = deck.get_bottom_card()
    deck.keep_card(card)
    try:
        deck.shuffle()
    except Exception, e:
        print e

    cards = []
    for i in range(1, 4):
        cards.append(deck.get_bottom_card())
    
    hand = Hand(cards)
    player1 = Player("Emilie", hand, None)
    
    cards = []
    for i in range(1, 4):
        cards.append(deck.get_bottom_card())
    
    hand = Hand(cards)
    player2 = Player("Italo", hand, None)

    cards = []
    for i in range(1, 4):
        cards.append(deck.get_bottom_card())
    
    hand = Hand(cards)
    player3 = Player("Attany", hand, None)
    
    cards = []
    for i in range(1, 4):
        cards.append(deck.get_bottom_card())
    
    hand = Hand(cards)
    player4 = Player("Keli", hand, None)

    pair1 = {'player1': player1, 'player2': player2}
    pair_one = Pair('pair_one', pair1)
    pair2 = {'player1': player3, 'player2': player4}
    pair_two = Pair('pair_two', pair2)

    # # Throwing first card
    # hand.throw_card()
    # # print hand

    # # Throwing third card
    # hand.throw_card()
    # # print hand

    # # Throwing second card
    # hand.throw_card()
    # # print hand

    # try:
    #     print hand.throw_card()
    #     print hand
    # except Exception, e:
    #     print e
    # for i in range(1, 4):
    #     cards.append(deck.get_bottom_card())

    # hand = Hand(cards)
    # print hand

    # # Throwing first card
    # hand.throw_card()
    # print hand

    # # Throwing third card
    # hand.throw_card()
    # print hand

    # # Throwing second card
    # hand.throw_card()
    # print hand

    # try:
    #     print hand.throw_card()
    #     print hand
    # except Exception, e:
    #     print e




