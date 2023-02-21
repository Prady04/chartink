import collections
import random

PlayingCard = collections.namedtuple(*card’, [‘suit’, ‘rank"])

class PlayingDeck:

   

ranks = [str(rank) for rank in range(2, 11)] + ["J"
suits = ['Spades", ‘Diamonds’, ‘Hearts’, ‘Clubs"]
def init__(self):

  

self._cards = [PlayingCard(rank, suit)
for suit in self.suits
for rank in self.ranks]

def _len_(self):
return len(self._cards)

def __getitem_(self, position):
return self._cards[position]

 

if _name__ == '_main_
deck = PlayingDeck()

   

#1. Slicing a deck
first_cut = deck[:4]

 

#2. Iterating through a deck
for card in deck:
  print(card)

#3. Iterating through the deck in reverse
for card in reversed(deck):

  print(card)

#4. Shuffling the deck

 
