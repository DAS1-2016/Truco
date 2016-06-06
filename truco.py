

class Card():
	"""Class for Card"""
	def __init__(self, suit, value=None):
		self.suit = suit
		self.value = value
	
	def clone(self, value):
		return Card(self.suit, value)


# if __name__ == '__main__':
# 	cardCopas = Card("Copas")
# 	card = cardCopas.clone("2")
# 	print "Card 1"
# 	print card.suit
# 	print card.value
# 	card2 = cardCopas.clone("3")
# 	print "Card 2"
# 	print card2.suit
# 	print card2.value