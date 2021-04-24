import random
import os
os.system('cls')
choices = ["rock","paper","scissors","spock", "lizard"]
cont = 'y'
count = 0
countWin = 0
while cont == 'y':
    count = count + 1
    computerChoice = random.choice(choices)
    playerChoice = input("Player, what's your choice? [ro/pa/sc/sp/li]")

    print(f"Computer choice is: {computerChoice}")
    print(f"Player's' choice is: {playerChoice}")

    if computerChoice[:2] == playerChoice:
        print("Tie.")
    elif ((playerChoice == 'ro' and (computerChoice == 'scissors' or computerChoice == 'lizard'))
        or (playerChoice == 'sc' and (computerChoice == 'paper' or  computerChoice == 'lizard'))
        or (playerChoice == 'pa' and computerChoice == 'rock')
        or (playerChoice == 'li' and (computerChoice == 'paper' or computerChoice == 'spock'))
        or (playerChoice == 'sp' and (computerChoice == 'rock' or  computerChoice == 'scissors' or computerChoice == 'paper'))):
        print("you win!") 
        countWin = countWin + 1
        
    else:
        print("You lost.")
    cont = input("Do you want to keep going? (y/n)")
print(f"Goodbye. You won {countWin} time(s). You played {count} time(s).")
