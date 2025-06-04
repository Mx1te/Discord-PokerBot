
from random import shuffle
from collections import Counter


# initialisiere alle wichtigen Listen

deck = []         # Speichert Karten im Deck
tableCards = []   # Speichert Karten auf Tisch
handRanking = []  # Speichert Ranking der Spielerhände
Players = []      # Speichert alle Spieler im Spiel  

#Classe für die Poker Karten

class pokerCard:

    # init für Karte

    def __init__(self, face, value, symbol):
        self.face = face        # Farbe(♠,♥,♦,♣)
        self.value = value      # Kartenwert(1-14)
        self.symbol = symbol    # Symbol(1-10,J,Q,K,A)
        deck.append(self)
    
    # func zum erstellen eines Decks

    def create_deck():
        deck.clear()
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


class Player:


    def __init__(self,id,hand):
        self.id = id
        self.hand = hand
        self.handranking = 0
        self.finalhand = []
        Players.append(self)

    def setRanking(self,ranking,finalhand):
        self.handranking = ranking
        self.finalhand = finalhand


## Hilfsfunktionen ##

def shuffleDeck():     #mischt Deck
        shuffle(deck)
    

def giveHoleCards(numPlayer):   # gibt Spielern Karten
    x = 1
    while x <= numPlayer:
        playerHand = [deck.pop(),deck.pop()]
        
        Player(x, playerHand)
        x += 1


def giveFlop():     # legt ersten 3 Karten auf den Tisch
    tableCards.clear()
    deck.pop()
    for x in range(3):
        tableCards.append(deck.pop())


def giveStreetCard():   # legt eine weitere Karte auf Tisch
    deck.pop()
    tableCards.append(deck.pop())


def setTableCards(card_list):
    """
    card_list: Liste von Tupeln im Format (face, value, symbol)
    Beispiel: [("hearts", 10, "10"), ("spades", 11, "Jack")]
    """
    tableCards.clear()
    for face, value, symbol in card_list:
        card = pokerCard(face, value, symbol)
        tableCards.append(card)


def setPlayerHand(player_id, card_list):
    """
    card_list: Liste von Tupeln (face, value, symbol)
    """
    # Spieler finden
    player = next((p for p in Players if p.id == player_id), None)
    if player:
        hand = []
        for face, value, symbol in card_list:
            card = pokerCard(face, value, symbol)
            hand.append(card)
        player.hand = hand


def checkForDoTrQu(hand:list):     #Prüft nach Pair/ThreeofKind/Quads
    # Hole alle Kartenwerte
    values = [card.value for card in hand]

    # Zähle, wie oft jeder Wert vorkommt
    valueCount = Counter(values)

    # Finde alle Kartenobjekte, die zu Duplikaten gehören
    pair_cards = [card for card in hand if valueCount[card.value] == 2]
    triple_cards = [card for card in hand if valueCount[card.value] == 3]
    quad_cards = [card for card in hand if valueCount[card.value] == 4]

    return {
        "pairs": pair_cards,
        "triples": triple_cards,
        "quads": quad_cards
    }

def checkForStraight(hand: list):
    # Extract and deduplicate values
    values = sorted(set([card.value for card in hand]))

    longest_streak = []
    temp_streak = [values[0]]

    for i in range(1, len(values)):
        if values[i] == values[i-1] + 1:
            temp_streak.append(values[i])
        else:
            if len(temp_streak) >= 5:
                longest_streak = temp_streak[:]
            temp_streak = [values[i]]

    if len(temp_streak) >= 5:
        longest_streak = temp_streak

    if longest_streak:
        # Find corresponding card objects (prioritize highest cards)
        straight_cards = []
        for v in reversed(longest_streak):  # from high to low
            for c in sorted(hand, key=lambda c: -c.value):
                if c.value == v and c not in straight_cards:
                    straight_cards.append(c)
                    break
            if len(straight_cards) == 5:
                break

        return straight_cards
    return None

def checkHands():
    
    i = 1

    for p in Players:
        StraightFlush = False
        FaceCheck = []

        HandToCheck = p.hand + tableCards

        ergebnis = checkForDoTrQu(HandToCheck)
        straight = checkForStraight(HandToCheck)

       # for x in straight:
       #     FaceCheck.append(x)
       #     if FaceCheck[FaceCheck.index(x)]

        if ergebnis["quads"]:
            p.setRanking(8, ergebnis["quads"])
        elif ergebnis["triples"] and ergebnis["pairs"]:
            p.setRanking(7, ergebnis["triples"] + ergebnis["pairs"])
        elif straight:
            p.setRanking(5, straight)
        elif ergebnis["triples"]:
            p.setRanking(4, ergebnis["triples"])
        elif len(set([c.value for c in ergebnis["pairs"]])) >= 2:
            p.setRanking(3, ergebnis["pairs"])  # Doppelpaar
        elif ergebnis["pairs"]:
            p.setRanking(2, ergebnis["pairs"])  # Ein Paar

        print()


pokerCard.create_deck()

shuffleDeck()

numPlayer = input("Spielerzahl: ")

giveHoleCards(int(numPlayer))

print("Spieler Karten in der Hand:")

for player in Players:
    print(f"Spieler {player.id}: ", end="")
    print(" ".join([card.face + card.symbol for card in player.hand]))

giveFlop()
giveStreetCard()
giveStreetCard()

setTableCards([
    ("hearts", 9, "9"),
    ("spades", 9, "9"),
    ("clubs", 9, "9"),
    ("diamonds", 11, "Jack"),
    ("hearts", 11, "Jack")
])

print("Gemeinsame Karten auf dem Tisch:")
for x in tableCards:
    print(x.face + x.symbol)

print("\n### Spielerhände prüfen ###")
checkHands()


ranking_namen = {
    0: "Keine Wertung",
    2: "Paar",
    3: "Doppelpaar",
    4: "Drilling",
    5: "Straße",
    7: "Full House",
    8: "Vierling"
}

for player in Players:
    rang = ranking_namen.get(player.handranking, f"Unbekannt ({player.handranking})")
    print(f"Spieler {player.id}: {rang} →", end=" ")
    print(" ".join([card.face + card.symbol for card in player.finalhand]))