import random
import sqlite3
import os

if not os.path.isfile('Score.db'):
    score_db = sqlite3.connect("Score.db")
    c = score_db.cursor()
    c.execute('''CREATE TABLE Scores
    (name text,
    score int)
    ''')
    score_db.commit()

score_db = sqlite3.connect("Score.db")

def deal():
    cards = []
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    rand_cards = []
    for i in range(0, 4):
        # create a 2d list of every possible card value
        # each inner list represents a different suit
        cards.append(['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king'])
    for i in range(0, 7):
        suit = random.randint(0, 3) 
        card = random.randint(0, len(cards[suit])-1)
        # append chosen card to list which will be returned at the end
        rand_cards.append(cards[suit][card] + ' of ' + suits[suit])
        # remove this card from the correct list to ensure it is not picked again
        cards[suit].remove(cards[suit][card])
    return rand_cards

def get_input(i):
    if i < 6:
        print('Card: ' + rand_cards[i])
        return input('Higher or lower? [h] or [l]: ')
    else:
        print('Card: ' + rand_cards[i])

def check_guess(guess):
    global total_score

    while guess != 'h' and guess != 'l':
        guess = input("Guess invalid, try again: ") 
    
    deck = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king'] 
    
    curr_card = deck.index(''.join(rand_cards[i].split(' ')[0]))
    next_card = deck.index(''.join(rand_cards[i+1].split(' ')[0]))

    if guess == 'h':
        if  curr_card < next_card:
            print("Correct")
            total_score += 10
        elif curr_card == next_card:
            print("Equal")
            total_score += 2
        else:
            print("Incorrect")
            total_score -= 5
    elif guess == 'l':
        if curr_card > next_card:
            print("Correct")
            total_score += 10
        elif curr_card == next_card:
            print("Equal")
            total_score += 2
        else:
            print("Incorrect")
            total_score -= 5
def change(lst):
    rand_cards = lst
    print("Card: "+ rand_cards[0])
    change = input("Would you like to change the card? [y] or [n]: ")
    if change == 'y':
        rand_cards[0] = deal()[0]
    else:
        rand_cards[0] = rand_cards[0] 
    return rand_cards

def save_display_score(name, score):
    score_db.execute('INSERT INTO Scores VALUES (?, ?);',
                     (name,
                      score))
                     
    for row in score_db.execute('SELECT * FROM Scores'):
        print(row)
        
play = True
while play:
    print('Welcome to this Higher or Lower game')
    print('-----------------------------')
    print('You are dealt 7 cards, and you must guess if the next one is higher or lower')
    print('Ok, let\'s begin:')
    
    rand_cards = deal()
    rand_cards = change(rand_cards)
    total_score = 0
    
    for i in range(0, 6):
        check_guess(get_input(i))
    get_input(6)

    print('Total score: ' + str(total_score))
    save_y = input("Would you like to save your score?: ")
    if save_y == 'yes':
        name = input("What is your name?: ")
        save_display_score(name, total_score)
    print('-----------------------------')

    while True:
        again = input('Do you want to play again? [y] or [n]: ') 
        if again == 'n':
            play = False
            break
        elif again == 'y':
            play = True
            print('-----------------------------')
            break
        else:
            print('Invalid. Try again.')
        
score_db.close()
