
from random import shuffle


deck = []
playerHands = []
tableCards = []


class pokerCard:

    def __init__(self,face,value):
        self.face = face
        self.value = value
        deck.append(self)
    
    def create_deck():
        deck.clear
        for i in range(1,11):
            pokerCard('diamonds'+str(i),i)
            pokerCard('clubs'+str(i),i)
            pokerCard('hearts'+str(i),i)
            pokerCard('spades'+str(i),i)

        pictureCards = ['Jack','Queen','King','Ace']
        i = 11

        for x in pictureCards:
            pokerCard('diamonds' + x, i)
            pokerCard('clubs' + x, i)
            pokerCard('hearts' + x, i)
            pokerCard('spades' + x, i)
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
    print(x.face)
    print(y.face)
    

giveFlop()

print('~~~~~~~~~')

for x in tableCards:
    print(x.face)
