# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = True
deal_ok = True
score = 0
who_bust = ''
who_win = ''

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
     
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return 'Hand contains ' + " ".join(str(x) for x in self.hand)
            
    def add_card(self, card):
        self.hand.append(card) # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.hand_value = sum([VALUES[x.rank] for x in self.hand])
        
        if not any([x.rank == 'A' for x in self.hand]):
            return self.hand_value
        elif self.hand_value !=0 and self.hand_value + 10 <= 21:
            return self.hand_value+10
        else:
            return self.hand_value  
       
    def draw(self, canvas, pos):
        for i in self.hand:
            i.draw(canvas, [pos[0]+self.hand.index(i)*CARD_SIZE[0],pos[1]])
               
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(i, x) for i in SUITS for x in RANKS]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.deck)   # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        return 'Deck contains ' + " ".join(str(x) for x in self.deck)	# return a string representing the deck       

#define event handlers for buttons
def deal():
    global outcome, in_play, GAME_DECK, PLAYER_HAND, DEALER_HAND, who_win, who_bust, score, deal_ok
    # your code goes here
    if deal_ok == False:
        who_bust = 'Hand Forfeit'
        score -= 1
    else:
        who_bust = ''
        
    GAME_DECK=Deck()
    GAME_DECK.shuffle()
    
    PLAYER_HAND = Hand()
    DEALER_HAND = Hand()
    
    PLAYER_HAND.add_card(GAME_DECK.deal_card())
    PLAYER_HAND.add_card(GAME_DECK.deal_card())
    DEALER_HAND.add_card(GAME_DECK.deal_card())
    DEALER_HAND.add_card(GAME_DECK.deal_card())
    
    if DEALER_HAND.get_value() == 21:
        who_win = 'Dealer Wins'
        in_play = False
        score -= 1
    
    in_play = True
    
    who_win = ''
    deal_ok = False
    
def hit():
    global PLAYER_HAND, in_play, who_bust, score, deal_ok
    # if the hand is in play, hit the player
    deal_ok = False
    who_bust = ''
    if in_play:
        PLAYER_HAND.add_card(GAME_DECK.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if PLAYER_HAND.get_value() > 21:
            in_play = False
            who_bust = 'Player Busted'
            score -= 1
            deal_ok = True
def stand():
    global DEALER_HAND, score, in_play, who_win, who_bust, deal_ok
    # replace with your code below
    deal_ok = True
    who_bust = ''
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while DEALER_HAND.get_value() < 17:
            DEALER_HAND.add_card(GAME_DECK.deal_card())
            if DEALER_HAND.get_value() > 21:
                who_bust = 'Dealer Busted'
                in_play = False
                deal_ok = True
        # assign a message to outcome, update in_play and score
        if DEALER_HAND.get_value() >= PLAYER_HAND.get_value() and DEALER_HAND.get_value() <= 21:
            who_win = 'Dealer Wins'
            in_play = False
            score -= 1
            deal_ok = True
        else:
            in_play = False
            score += 1
            who_win ='Player Wins'
            deal_ok = True
    
# draw handler    
def draw(canvas):
    canvas.draw_text('BlackJack', (75, 75), 40, 'Maroon', 'sans-serif')
    canvas.draw_text('Score '+ str(score), (400, 75), 30, 'Black', 'sans-serif')
    canvas.draw_text('Dealer', (60, 150), 30, 'Black', 'sans-serif')
    canvas.draw_text('Player', (60, 400), 30, 'Black', 'sans-serif')
    canvas.draw_text(who_win, (200, 150), 30, 'White', 'sans-serif')
    canvas.draw_text(who_bust, (200, 580), 30, 'White', 'sans-serif')
    
    PLAYER_HAND.draw(canvas, [60,450])
    DEALER_HAND.draw(canvas, [60,200])   
   
    if in_play:
        canvas.draw_text('Hit or Stand?', (250, 400), 30, 'Black', 'sans-serif')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [60 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
        canvas.draw_text('New Deal?', (250, 400), 30, 'Black', 'sans-serif')
                         
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
