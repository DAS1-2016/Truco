import pytest
from truco import Card, Deck, Hand, CardCheck

@pytest.fixture
def deck():
    Deck.instance = None
    return Deck.get_instance()

class TestCard:

    @pytest.fixture
    def card(self):
        return Card("Copas", "3")

    def test_card_clone(self, card):
        new_card = card.clone("J")
        assert new_card.suit == card.suit
        assert new_card.value == "J"


class TestDeck:

    NUMBER_OF_CARDS_IN_TRUCO = 40

    def test_deck_initialization(self, deck):
        assert len(deck.cards) == self.NUMBER_OF_CARDS_IN_TRUCO

    def test_get_top_card(self, deck):
        top_card = deck.cards[0]
        assert deck.get_top_card() == top_card
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)

    def test_get_bottom_card(self, deck):
        bottom_card = deck.cards[len(deck.cards) - 1]
        assert deck.get_bottom_card() == bottom_card
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)

    def test_keep_card(self, deck):
        bottom_card = deck.get_bottom_card()
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)
        deck.keep_card(bottom_card)
        assert len(deck.cards) == self.NUMBER_OF_CARDS_IN_TRUCO

    def test_shuffle(self, deck):
        try:
            deck.shuffle()
            shuffled = True
        except Exception:
            shuffled = False
        assert shuffled

    def test_shuffle_without_a_card(self, deck):
        bottom_card = deck.get_bottom_card()
        try:
            deck.shuffle()
            shuffled = True
        except Exception:
            shuffled = False
        assert not shuffled


class TestHand:

    @pytest.fixture
    def hand(self, deck):
        cards = []
        for i in range(1, 4):
            cards.append(deck.get_bottom_card())
        return Hand(cards)

    @pytest.fixture
    def fixed_hand(self):
        self.card1 = Card("Espadas", "A")
        self.card2 = self.card1.clone("3")
        self.card3 = self.card1.clone("2")
        cards = []
        cards.append(self.card1)
        cards.append(self.card2)
        cards.append(self.card3)
        return Hand(cards)

    def test_throw_one_card(self, hand):
        assert len(hand.cards) == 3
        hand.throw_card()
        assert len(hand.cards) == 2

    def test_throw_two_card(self, hand):
        assert len(hand.cards) == 3
        hand.throw_card()
        hand.throw_card()
        assert len(hand.cards) == 1

    def test_throw_two_card(self, hand):
        assert len(hand.cards) == 3
        hand.throw_card()
        hand.throw_card()
        hand.throw_card()
        assert len(hand.cards) == 0

    def test_throw_first_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

    def test_throw_second_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards

    def test_throw_third_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards

    def test_throw_card_on_position_out_of_range(self, fixed_hand):
        fixed_hand.throw_card(10)
        assert self.card1 not in fixed_hand.cards

    def test_throw_first_then_second_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards
        fixed_hand.throw_card(2)
        assert self.card3 not in fixed_hand.cards

    def test_throw_first_then_third_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards
        fixed_hand.throw_card(3)
        assert self.card2 not in fixed_hand.cards

    def test_throw_second_then_first_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

    def test_throw_second_then_third_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards
        fixed_hand.throw_card(3)
        assert self.card1 not in fixed_hand.cards

    def test_throw_third_then_second_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards

    def test_throw_third_then_first_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

class TestCardCheck:

    @pytest.fixture
    def suits(self):
        cards = {}
        cards['spades'] = Card("Espadas")
        cards['clubs'] = Card("Paus")
        cards['hearts'] = Card("Copas")
        cards['diamonds'] = Card("Ouros")

        return cards

    @pytest.fixture
    def shackles(self, suits):
        hearts = suits['hearts'].clone("7")
        zap = suits['clubs'].clone("4")
        diamonds = suits['diamonds'].clone("7")
        ace_of_spades = suits['spades'].clone("A")
        
        shackles = []
        shackles.append(zap)
        shackles.append(hearts)
        shackles.append(diamonds)
        shackles.append(ace_of_spades)
        
        return shackles

    def get_winner_on_card_check(self, pair_one, pair_two):
        round_cards = {'pair_one': pair_one, 'pair_two':pair_two}
        card_check = CardCheck(round_cards)
        result = card_check.get_winner()
        return result

    def test_card_check_with_all_shackles(self, shackles):
        
        pair_one = [shackles[0], shackles[3]]
        pair_two = [shackles[1], shackles[2]]
        
        expected = shackles[0]
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result.value is expected.value
        assert result.suit is expected.suit

    def test_card_check_with_one_shackle_on_each_pair(self, shackles, suits):
        normal_card = suits['spades'].clone("3")
        pair_one = [shackles[1], normal_card]
        pair_two = [shackles[3], normal_card] 

        expected = shackles[1]
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result.value is expected.value
        assert result.suit is expected.suit

    def test_card_check_without_shackles(self, suits):
        card1 = suits['spades'].clone("3") 
        card2 = suits['clubs'].clone("J") 
        card3 = suits['diamonds'].clone("2") 
        card4 = suits['hearts'].clone("A") 
        
        pair_one = [card1, card2]
        pair_two = [card3, card4] 

        expected = card1
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result.value is expected.value
        assert result.suit is expected.suit
