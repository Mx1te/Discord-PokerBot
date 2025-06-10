
from random import shuffle
from collections import Counter


# initialisiere alle wichtigen Listen

deck = []         # Speichert Karten im Deck
tableCards = []   # Speichert Karten auf Tisch
Players = []      # Speichert alle Spieler im Spiel  

#Klasse für die Poker Karten

class PokerCard:

    # init für Karte

    def __init__(self, face, value, symbol, add_to_deck=True):
        self.face = face        # Farbe(♠,♥,♦,♣)
        self.value = value      # Kartenwert(1-14)
        self.symbol = symbol    # Symbol(1-10,J,Q,K,A)
        deck.append(self)
    
    # func zum erstellen eines Decks

    @staticmethod
    def create_deck():
        deck.clear()
        for i in range(1,11):
            PokerCard('diamonds',i,str(i))
            PokerCard('clubs',i,str(i))
            PokerCard('hearts',i,str(i))
            PokerCard('spades',i,str(i))

        pictureCards = ['Jack','Queen','King','Ace']
        i = 11

        for x in pictureCards:
            PokerCard('diamonds', i, x)
            PokerCard('clubs' , i, x)
            PokerCard('hearts' , i, x)
            PokerCard('spades' , i, x)
            i += 1


class Player:


    def __init__(self,id,hand):
        self.id = id
        self.hand = hand
        self.handvalue = check_value(hand)
        self.handranking = 0
        self.finalhand = []
        self.finalhandvalue = 0
        Players.append(self)

    def setRanking(self,ranking,finalhand):
        self.handranking = ranking
        self.finalhand = finalhand
        self. finalhandvalue = check_value(finalhand)


## Hilfsfunktionen ##

def shuffle_deck():     #mischt Deck
        shuffle(deck)
    

def give_hole_cards(numPlayer):   # gibt Spielern Karten
    Players.clear()
    x = 1
    while x <= numPlayer:
        playerHand = [deck.pop(),deck.pop()]
        
        Player(x, playerHand)
        x += 1


def give_flop():     # legt ersten 3 Karten auf den Tisch
    tableCards.clear()
    deck.pop()
    for x in range(3):
        tableCards.append(deck.pop())


def give_street_card():   # legt eine weitere Karte auf Tisch
    deck.pop()
    tableCards.append(deck.pop())


def set_tableCards(card_list):
    """
    card_list: Liste von Tupeln im Format (face, value, symbol)
    Beispiel: [("hearts", 10, "10"), ("spades", 11, "Jack")]
    """
    tableCards.clear()
    for face, value, symbol in card_list:
        card = PokerCard(face, value, symbol, add_to_deck=False)
        tableCards.append(card)


def set_player_hand(player_id, card_list):
    """
    card_list: Liste von Tupeln (face, value, symbol)
    """
    # Spieler finden
    player = next((p for p in Players if p.id == player_id), None)
    if player:
        hand = []
        for face, value, symbol in card_list:
            card = PokerCard(face, value, symbol, add_to_deck=False)
            hand.append(card)
            player.hand = hand


def check_for_do_tr_qu(hand:list):     #Prüft nach Pair/ThreeofKind/Quads
    # Hole alle Kartenwerte
    values = [card.value for card in hand]

    # Zähle, wie oft jeder Wert vorkommt
    valueCount = Counter(values)

    # Finde alle Kartenobjekte, die zu Duplikaten gehören
    
    return {
        "pairs": [card for card in hand if valueCount[card.value] == 2],
        "triples": [card for card in hand if valueCount[card.value] == 3],
        "quads": [card for card in hand if valueCount[card.value] == 4]
    }


def check_for_straight(hand: list):

    # Extract and deduplicate values
    values = sorted(set([card.value for card in hand]))

    # Nach sortiertem Set: [2, 3, 4, 5, 14] → Ace als 1 behandeln
    if 14 in values:
        values.insert(0, 1)

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


def check_for_flush(hand:list):
    try:
        faces = [card.face for card in hand]

        faceCount = Counter(faces)

        flushCards = [card for card in hand if faceCount[card.face] >= 5]

        if flushCards:
            return sorted(flushCards, key=lambda c: c.value, reverse=True)[:5]
    except:
        return None


def check_value(Hand:list):
    return sum(card.value for card in Hand)


def compare_hands(player1, player2):
    hand1 = sorted(player1.finalhand, key=lambda c: c.value, reverse=True)
    hand2 = sorted(player2.finalhand, key=lambda c: c.value, reverse=True)

    for c1, c2 in zip(hand1, hand2):
        if c1.value > c2.value:
            return player1
        elif c2.value > c1.value:
            return player2
    return None  # Tie


def check_hands():

    for p in Players:
        
        StraightFlush = None
        RoyalFlush = False

        HandToCheck = p.hand + tableCards

        DoTrQu = check_for_do_tr_qu(HandToCheck)
        straight = check_for_straight(HandToCheck)
        flush = check_for_flush(HandToCheck)

        # Filtere nur Straight-Karten mit der Flush-Farbe
        flush_straight = []
        if flush and straight:
            flush_face = flush[0].face
            flush_straight = [c for c in straight if c.face == flush_face]

        if len(flush_straight) == 5:
            StraightFlush = flush_straight
            if set(c.value for c in flush_straight) == {10, 11, 12, 13, 14}:
                RoyalFlush = True

        trip_values = sorted(set(c.value for c in DoTrQu["triples"]), reverse=True)
        pair_values = sorted(set(c.value for c in DoTrQu["pairs"]), reverse=True)

        if RoyalFlush:
            p.setRanking(10,StraightFlush)
        elif StraightFlush:
            p.setRanking(9,StraightFlush)
        elif DoTrQu["quads"]:
            p.setRanking(8, DoTrQu["quads"])
        if len(trip_values) >= 2:
            p.setRanking(7, 
                [c for c in DoTrQu["triples"] if c.value == trip_values[0]] + 
                [c for c in DoTrQu["triples"] if c.value == trip_values[1]][:2])
        elif trip_values and pair_values:
            p.setRanking(7, 
                [c for c in DoTrQu["triples"] if c.value == trip_values[0]] + 
                [c for c in DoTrQu["pairs"] if c.value == pair_values[0]][:2])
        elif flush:
            p.setRanking(6,flush)
        elif straight:
            p.setRanking(5, straight)
        elif DoTrQu["triples"]:
            p.setRanking(4, DoTrQu["triples"])
        elif len(set([c.value for c in DoTrQu["pairs"]])) >= 2:
            p.setRanking(3, DoTrQu["pairs"])  
        elif DoTrQu["pairs"]:
            p.setRanking(2, DoTrQu["pairs"])
        else:
            best = sorted(p.hand, key=lambda c: c.value, reverse=True)[:5]
            p.setRanking(1, best)  


def check_winner():
    maxRanking = max(set([p.handranking for p in Players]))
    
    Winners = [player for player in Players if player.handranking == maxRanking]

    if len(Winners) > 1:
        maxValue = max(set([p.finalhandvalue for p in Winners]))

        Winners = [player for player in Winners if player.finalhandvalue == maxValue]

        if len(Winners) > 1:
            best = Winners[0]
            for contender in Winners[1:]:
                winner = compare_hands(best, contender)
                if winner == contender:
                    best = contender
            print(f"\n→ Der Gewinner ist Spieler {best.id}")
        else:
            print(f"\n→ Der Gewinner ist Spieler {Winners[0].id}")
    else:
        print(f"\n→ Der Gewinner ist Spieler {Winners[0].id}")


PokerCard.create_deck()

shuffle_deck()

numPlayer = input("Spielerzahl: ")

give_hole_cards(int(numPlayer))

print("Spieler Karten in der Hand:")

for player in Players:
    print(f"Spieler {player.id}: ", end="")
    print(" ".join([card.face + card.symbol for card in player.hand]))

give_flop()
give_street_card()
give_street_card()



print("Gemeinsame Karten auf dem Tisch:")
for x in tableCards:
    print(x.face + x.symbol)

print("\n### Spielerhände prüfen ###")
check_hands()


ranking_namen = {
    0: "Keine Wertung",
    1: "High Card",
    2: "Paar",
    3: "Doppelpaar",
    4: "Drilling",
    5: "Straße",
    6: "Flush",
    7: "Full House",
    8: "Vierling",
    9: "Straight Flush",
    10: "Royal Flush"
}

for player in Players:
    rang = ranking_namen.get(player.handranking, f"Unbekannt ({player.handranking})")
    print(f"Spieler {player.id}: {rang} →", end=" ")
    print(" ".join([card.face + card.symbol for card in player.finalhand]))


check_winner()