# -*- coding: utf-8 -*- 
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
        print(len(self.cards))
        if len(self.cards) is not self.CARDS_QUANTITY:
            raise Exception('Alguem esta roubando e nao devolveu todas as cartas!')

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
        self.winner = self.check_winner_round()
    
    def get_winner(self):
        return self.winner

    def check_winner_round(self):
        winners_pairs = []

        pair_one_winner = self.check_shackles(self.round_cards[Pair.PAIR_ONE_ID])
        winners_pairs.append(pair_one_winner)
        pair_two_winner = self.check_shackles(self.round_cards[Pair.PAIR_TWO_ID])
        winners_pairs.append(pair_two_winner)
        
        winner_card = self.check_shackles(winners_pairs)  
        if winner_card in self.round_cards[Pair.PAIR_ONE_ID]:
            winner = Pair.PAIR_ONE_ID
        else: 
            winner = Pair.PAIR_TWO_ID
        return winner

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

    def __init__(self, player_name):
        self.player_name = player_name
        self.hand = None

    def throw_card(self, match, card_position=1):
        card = self.hand.throw_card(card_position)
        print self.player_name + " jogando carta " + str(card)
        match.receive_card(self, card)

class Pair(object):
    """ Represents the pair """
    
    PAIR_ONE_ID = 'pair_one'
    PAIR_TWO_ID = 'pair_two'

    def __init__(self, id_pair, players):
        self.id_pair = id_pair
        self.players = players

    players = {}.fromkeys(['player1','player2'],'player')


class Game(object):
    """Represents the Game"""
    def __init__(self, pairs):
        self.pairs = pairs
        self.score = {Pair.PAIR_ONE_ID: 0, Pair.PAIR_TWO_ID: 0}
        self.current_match = Match(self)
        self.matches = []

    def start(self):
        self.current_match.start_match()

    def end_current_match(self, pair=None):

        if not pair:
            winner = self.current_match.end_match()
        else:
            winner = pair

        if winner is Pair.PAIR_ONE_ID:
            self.score[Pair.PAIR_ONE_ID] += self.current_match.state.get_points()
        else:
            self.score[Pair.PAIR_TWO_ID] += self.current_match.state.get_points()
        self.__next_match()

    def colect_cards(self):
        print
        print "Colecting cards..."
        self.colect_round_cards()
        self.colect_players_cards()

    def colect_players_cards(self):
        for pair in self.pairs:
            for player in pair.players:
                for card in pair.players[player].hand.cards:
                    Deck.get_instance().keep_card(card)

    def colect_round_cards(self):
        for rnd in self.current_match.rounds:
            for player in rnd.round_cards:
                Deck.get_instance().keep_card(rnd.round_cards[player])

    def __next_match(self):
        self.colect_cards()
        self.matches.append(self.current_match)
        # Starts a new match
        self.current_match = Match(self)
        self.current_match.start_match()

class Round:

    def __init__(self, match):
        self.match = match
        self.round_cards = {}

    def add_round_card(self, player, card):
        self.round_cards[player] = card

    def end_round(self):
    
        player1 = self.match.game.pairs[0].players['player1']
        player2 = self.match.game.pairs[0].players['player2']
        player3 = self.match.game.pairs[1].players['player1']
        player4 = self.match.game.pairs[1].players['player2']
        cards_pair_one = (self.round_cards[player1],self.round_cards[player2])
        cards_pair_two = (self.round_cards[player3],self.round_cards[player4])
        pair_round_cards = {Pair.PAIR_ONE_ID:cards_pair_one,Pair.PAIR_TWO_ID:cards_pair_two}
        self.card_checker = CardCheck(pair_round_cards)
        winner = self.card_checker.get_winner()
        return winner


class MatchState:

    def __init__(self, match):
        self.match = match

    @staticmethod
    def get_state_name():
        raise NotImplementedError
    
    def raise_match(self):
        raise NotImplementedError

    def get_points(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

class TwelveMatch(MatchState):

    MATCH_POINTS = 12
    
    def __init__(self, match):
        MatchState.__init__(self, match)
    
    @staticmethod
    def get_state_name():
        return "Doze"

    def raise_match(self):
        raise Exception("Partida de 12, ou vai ou racha")

    def get_points(self):
        return self.MATCH_POINTS

    def next(self):
        raise Exception("Partida de 12, ou vai ou racha")

class NineMatch(MatchState):

    MATCH_POINTS = 9
    
    def __init__(self, match):
        MatchState.__init__(self, match)
    
    @staticmethod
    def get_state_name():
        return "Nove"

    def raise_match(self):
        self.match.set_state(TwelveMatch(self.match))

    def get_points(self):
        return self.MATCH_POINTS

    def next(self):
        return TwelveMatch


class SixMatch(MatchState):

    MATCH_POINTS = 6
    
    def __init__(self, match):
        MatchState.__init__(self, match)
    
    @staticmethod
    def get_state_name():
        return "Seis"

    def raise_match(self):
        self.match.set_state(NineMatch(self.match))

    def get_points(self):
        return self.MATCH_POINTS

    def next(self):
        return NineMatch

class TrucoMatch(MatchState):

    MATCH_POINTS = 3
    
    def __init__(self, match):
        MatchState.__init__(self, match)
    
    @staticmethod
    def get_state_name():
        return "Truco"

    def raise_match(self):
        self.match.set_state(SixMatch(self.match))

    def get_points(self):
        return self.MATCH_POINTS

    def next(self):
        return SixMatch

class NormalMatch(MatchState):

    MATCH_POINTS = 1
    
    def __init__(self, match):
        MatchState.__init__(self, match)

    @staticmethod
    def get_state_name():
        return "Normal"

    def raise_match(self):
        self.match.set_state(TrucoMatch(self.match))

    def get_points(self):
        return self.MATCH_POINTS

    def next(self):
        return TrucoMatch 

class Match:
    
    def __init__(self, game):
        self.game = game
        self.current_round = Round(self)
        self.rounds = []
        self.rounds_winners = []
        self.state = NormalMatch(self)

    def start_match(self):
        deck = Deck.get_instance()
        deck.shuffle()
        for pair in self.game.pairs:
            self.create_player_hand(pair.players['player1'])
            self.create_player_hand(pair.players['player2'])

    def set_state(self, state):
        self.state = state

    def create_player_hand(self, player):
        deck = Deck.get_instance()
        cards = []
        for i in range(1, 4):
            cards.append(deck.get_top_card())
        player.hand = Hand(cards) 

    def receive_card(self, player, card):
        self.current_round.add_round_card(player, card)

    def end_current_round(self):
        winner = self.current_round.end_round()
        self.rounds_winners.append(winner)
        self.rounds.append(self.current_round)
        if self.is_last_round():
            self.game.end_current_match()
        else:
            self.current_round = Round(self)

    def is_last_round(self):
        return len(self.rounds) == 3

    def raise_match(self, player):
        print("\n %s está pedindo %s \n" % (player.player_name, self.state.next().get_state_name()))
        pair = self.__get_player_pair(player)
        accept = self.__send_raise_request(pair[1])
        if(accept):
            self.state.raise_match()
        else:
            winner_pair_id = self.game.pairs[pair[0]].id_pair
            self.rounds.append(self.current_round)
            self.game.end_current_match(winner_pair_id)

    def __get_player_pair(self, player):

        player1_pair1 = player.player_name == self.game.pairs[0].players['player1'].player_name
        player2_pair1 = player.player_name == self.game.pairs[0].players['player2'].player_name         
        if  player1_pair1 or player2_pair1:
            pair = (0, 1)
        else:
            pair = (1, 0)
        return pair

    def __send_raise_request(self, target_pair):
        pair = self.game.pairs[target_pair].id_pair
        print pair
        if pair == Pair.PAIR_ONE_ID:
            pair_number = 'Par 1'
        else:
            pair_number = 'Par 2'

        message = pair_number + ' deseja aceitar o pedido de ' + self.state.next().get_state_name()
        accept = self.__get_pair_answer(message)

        return accept

    def __get_pair_answer(self, message):
        answer = raw_input(message + "\n" + "S - Sim/ N - Nao\n").lower()  
        if(answer == "s" or answer == "sim"):
            accept = True
        else:
            accept = False

        return accept

    def end_match(self):
        qnt_pair_one_winner = 0
        qnt_pair_two_winner = 0
        for winner in self.rounds_winners:
            if winner is Pair.PAIR_ONE_ID:
                qnt_pair_one_winner += 1
            else:
                qnt_pair_two_winner += 1

        if qnt_pair_one_winner >= 2:
            winner = Pair.PAIR_ONE_ID
        else: 
            winner = Pair.PAIR_TWO_ID
        return winner



