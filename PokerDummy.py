
from random import shuffle


deck = []
playerHands = []
tableCards = []


class pokerCard:

    def __init__(self, face, value, symbol):
        self.face = face
        self.value = value
        self.symbol = symbol
        deck.append(self)
    
    def create_deck():
        deck.clear
        for i in range(1,11):
            pokerCard('diamonds',i,str(i))
            pokerCard('clubs',i,str(i))
            pokerCard('hearts',i,str(i))
            pokerCard('spades',i,str(i))

        pictureCards = ['Jack','Queen','King','Ace']
        i = 11

        for x in pictureCards:
            pokerCard('diamonds', i, x)
            pokerCard('clubs' , i, x)
            pokerCard('hearts' , i, x)
            pokerCard('spades' , i, x)
            i += 1


def shuffle_deck():
        shuffle(deck)
    
def giveHoleCards(numPlayer):
    playerHands.clear
    x = 1
    while x <= numPlayer:
        playerHands.append([deck.pop(),deck.pop()])
        x += 1
    
def giveFlop():
    tableCards.clear
    deck.pop()
    for x in range(3):
        tableCards.append(deck.pop())

def giveStreetCard():
    deck.pop()
    tableCards.append(deck.pop())


pokerCard.create_deck()

shuffle_deck()

numPlayer = int(input("Enter player number: "))

giveHoleCards(numPlayer)

for x, y in playerHands:
    print('------')
    print(x.face + x.symbol)
    print(y.face + y.symbol)
    

giveFlop()

print('~~~~~~~~~')

for x in tableCards:
    print(x.face + x.symbol)
