import pytest
from truco import Card, Deck


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

    @pytest.fixture
    def deck(self):
        Deck.instance = None
        return Deck.get_instance()

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


