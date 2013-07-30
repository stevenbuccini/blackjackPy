##################
#### Blackjack ###
##################
# Author: Steven Buccini
# Built with love specifically for the Hacker School Fa13 application


#To-do
#1. Add ascii symbols for the suits
#2. Flesh out the methods according to comments
#Global Variables
#How should the deck work?  Global cariable?


from random import shuffle #import the shuffle method for shuffling cards
import os #will allow us to clear the terminal

MINIMUM_BET = 10
MAXIMUM_BET = 200
SUITS = {"H":"Hearts", "S":"Spades", "C": "Clubs", "D":"Diamonds"}
CARD_VALUES = {"Ace":[1,11], "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10}
deck = None #We want all objects to be able to know what's in the deck and what's not.
dealer = None #Dealer's hand should be accessible to all players

class Card(object):
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value
	def __str__(self):
		return str(self.value)+ " of "+SUITS[self.suit]
	def __repr__(self):
		return str(self.value)+ " " + self.suit

	def get_numeric_value(self):
		return CARD_VALUES[self.value]
	def set_numeric_value(self, value):
		"""Used to set the value of the Ace"""
		if self.value != "Ace":
			return "Error: we can only change the value of the Ace"
		else:
			CARD_VALUES["Ace"] = value
			return None

class Deck(object):
	"""We will arbitrarily let the top of the deck be the very last item in the deck"""
	
	def __init__(self):
		self.cards = []
		for suit in SUITS:
			for value in CARD_VALUES:
				self.cards.append(Card(suit, value))
	def shuffle_cards(self):
		return shuffle(self.cards) #RETURNS None! Works in place.
	def draw(self):
		return self.cards.pop() #return the topmost card


class Player(object):
	def __init__(self, name, startingCash):
		self.money = startingCash
		self.name = name
		self.hand = []
		current_bet = None
	#def __str__():
		#output player's information in a readable manner


	def action(self):
		choices = ["hit", "stay", "hold"]
		
		#Ensure that player hasn't busted yet
		if self.get_hand_value() > 21:
			return self.stay()
		if len(self.hand) == 2:
			""" Can't get split to work within time constraints, will sit and think for a bit.
			if self.hand[0].value == self.hand[1].value:
				choices.append(["doubledown", "split"])
				action = input("Would you like to HIT, STAY/HOLD, DOUBLE DOWN, or SPLIT?\n").lower().replace(" ", "")
				if action not in choices:
					print("Please enter either HIT, STAY/HOLD, DOUBLE DOWN, or SPLIT.")
					return self.action()
				else:
					if action == "hit":
						self.hit(deck)
						return self.action()
					elif action == "stay" or action == "hold":
						return self.stay()
					elif action == "doubledown":
						self.bet *= 2
						print("Your bet is now $" + self.bet)
						self.hit(deck)
						return self.action()
					elif action == "split":
						return "STILL NEED TO BUILD THIS OUT"
					else:
						return "Error: you shouldn't be here. Please restart the game."
			else:
			#Don't forget to inden't the line below when this feature is enabled!
			"""
			choices.append("doubledown")
			action = input("Would you like to HIT, STAY/HOLD, or DOUBLE DOWN?\n").lower().replace(" ", "")
			if action not in choices:
				print("Please enter either HIT, STAY/HOLD, or DOUBLE DOWN.")
				return self.action()
			if action == "hit":
				self.hit(deck)
				return self.action()
			elif action == "stay" or action == "hold":
				return self.stay()
			elif action == "doubledown":
				self.current_bet *= 2
				print("Your new bet is $" + str(self.current_bet))
				self.hit(deck)
				return self.stay()
			else:
				return "Error: you shouldn't be here. Please restart the game."
		else:
			action = input("Would you like to HIT or STAY/HOLD?\n").lower().replace(" ", "")
			if action not in choices:
				print("Please enter either HIT or STAY/HOLD.")
				return self.action()
			if action == "hit":
				self.hit(deck)
				return self.action()
			elif action == "stay" or action == "hold":
				return self.stay()
			else:
				return "Error: you shouldn't be here. Please restart the game."
		


	def stay(self):
		return self.hand
	def hit(self, deck):
		new_card = self.get_card(deck)
		dealer.show_hand(False)
		self.show_hand()
	def place_bet(self):
		#takes bet, ensures it is valid, then increments bet and decrements money
		try:
			bet = int(input("Please make your bet. You currently have: $"+str(self.money)+"\n"))
			#ensure that this bet is valid. Cascading if statements allow for recursion
			if bet > self.money:
				print("You don't have that much money.  Please try again.\n")
				bet = self.place_bet()
			if bet > MAXIMUM_BET:
				print("The maximum bet for this game is " + str(MAXIMUM_BET)+"\n")
				bet = self.place_bet()
			if bet < MINIMUM_BET:
				print("The minimum bet for this game is " + str(MINIMUM_BET)+"\n")
				bet = self.place_bet()
			self.current_bet = bet
			return bet
		except ValueError:
			print("You must bet an integer.")
			self.place_bet()

		return None
	def get_card(self, deck):
		new_card = deck.draw()
		if new_card.value == "Ace":
			valid = False
			while not valid:
				try:
					answer = int(input("What value do you want your Ace to be: 1 or 11?\n"))
					if answer != 1 and answer != 11:
						print("Ace can only have a value of 1 or 11. Please try again.")
					else:
						new_card.set_numeric_value(answer) #set the Ace's value to the desired choice
						valid = True #exit loop
				except ValueError:
					print("Answer must be an integer.")
		self.hand.append(new_card)
		return new_card
	def show_hand(self):
		print("You have:\n")
		for card in self.hand:
			print("\t* "+str(card)+"\n")
		print("Hand value: " + str(self.get_hand_value()))
	def get_hand_value(self):
		return sum(card.get_numeric_value() for card in self.hand) #This method probably won't work with the list comprehension

class Dealer(Player):
	def __init__(self):
		self.name = "Dealer"
		self.money = float("inf") #The house has infinite money because the house ALWAYS wins
		self.hand = []
	def action(self):
		#essentially is the same as the Player, but has AI for playing
		#The dealer's behavior is actually explicitly defined by the rules.
		if self.get_hand_value() < 17:
			self.hit(deck)
			return self.action()
		else:
			self.stay()

	def show_hand(self, hole_card = True):
		print("Dealer has:\n\t*"+str(self.hand[0])+"\n")
		if(hole_card):
			#players can only see the 
			for i in range(1, len(self.hand)):
				print("\t* "+str(self.hand[i]))
		#print("Dealer's hand value (UNCOMMENT AFTER DEBUGGING): " + str(self.get_hand_value()))
	def get_card(self, deck):
		current_hand_value = self.get_hand_value()
		new_card = deck.draw()
		if new_card.value == "Ace":
			if current_hand_value >= 11:
				new_card.set_numeric_value(1)
			elif len(self.hand) == 0:
				new_card.set_numeric_value(11)
			elif current_hand_value >= 6 and current_hand_value < 11:
				new_card.set_numeric_value(11)
			else:
				new_card.set_numeric_value(1)
		self.hand.append(new_card)
		return new_card
	def hit(self, deck):
		new_card = self.get_card(deck)
		dealer.show_hand()





def play_hand(player, dealer):
	global deck
	player_final_hands = {}
	deck = Deck() #build deck
	deck.shuffle_cards() # shuffle the cards
	player.place_bet() #get bets from all players who aren't dealers
	for i in range(2): #each player gets two cards to start
		player.get_card(deck)
		dealer.get_card(deck)
	dealer.show_hand(False)
	player.show_hand()
	player_final_hands[player.name] = player.action()
	dealer_hand = dealer.action()
	dealer.show_hand()
	determine_outcome(player, dealer)
	dealer.hand = [] #reset hands
	player.hand = [] #reset hands
	return None

def determine_outcome(player, dealer):
	#handles case where player has split his cards
	clear_screen()
	dealer.show_hand()
	player.show_hand()
	dealer_score = dealer.get_hand_value()
	player_score = player.get_hand_value()
	#print("Dealer Score: " + str(dealer_score) + " Player Score: " + str(player_score))
	if player_score > 21:
		player.money -= player.current_bet
		print("You busted!  You lost $" + str(player.current_bet) + " and have $" + str(player.money) + " remaining.")
		return None
	if player_score == 21 and len(player.hand) == 2:
		player.money  = ceil(1.5 * player.current_bet)
		print("Nice, natural blackjack! You get 1.5x your original bet of $" + str(player.current_bet) +" and currently have $" + player.money + " remaining")
		return None
	if dealer_score == 21:
		if player_score != 21:
			player.money -= player.current_bet
			print("Your hand of " + str(player_score) + " lost to the dealer's " + str(dealer_score) +". You lost $" + player.current_bet + " and have $" + player.money + " remaining.")
			return None
	elif dealer_score > 21:
		player.money += player.current_bet
		print("The dealer busted! You won $" + str(player.current_bet) + " and have $" + str(player.money) + " remaining.")
		return None
	elif player_score > dealer_score:
		player.money += player.current_bet
		print("You have more points than the dealer! You won $" + str(player.current_bet) + " and have $" + str(player.money) + " remaining.")
		return None
	elif player_score < dealer_score:
		player.money -= player.current_bet
		print("The dealer has more points than you. You lost $" + str(player.current_bet) + " and have $" + str(player.money) + " remaining.")
		return None
	else:
		print("Dealer and player have the same score; no money is gained or lost")
		return None
	return None

def help():
	print('You can type help at any time to access this information.\n' 
		  "1. Playing the game:  This game is similar to normal blackjack, but it's just you and the dealer.\n"
				"\t*You have several commands availble to you, depending on the context: STAY (or HOLD), HIT, and DOUBLE DOWN.\n"
				"\t*We do not currently support splitting, but that should be implemented soon!\n"
				"\t*You may only split or double down immediately after your hand has been dealt.\n"
				"\t*We don't play with insurance, and you can't surrender your hand.\n"
		  "2. Betting: Minimum bet is 10, maxiumum bet is 200.\n"
		  "3. Reminders:\n"
		  			"\t* An ace can have a value of either 1 or 11, but once its value is assigned it cannot be changed.\n"
			 		"\t* On natural blackjack (when you've been dealt blackjack), you earn 1.5x your bet.\n"
			 		"\t* Splitting is when you are dealt two cards with the same value. If you decide to split,\n"
			 		  "\t you will essentially be playing two hands, with each card in the original hand becoming\n"
			 		  "\t the first card in your two hands. NOTE: Since you can split cards of the same value, that\n"
			 		  "\t means you can split two cards with a value of ten even if they don't form a pair, e.g \n"
			 		  "\t you can split a Jack and a King because they both have a value of 10.\n"
			 		"\t* Doubling down allows you to double your bet if you are confident you can beat the dealer.\n"
			 		  "\t This can only be done immediately after you have been dealt your hand. You will only\n"
			 		  "\t recieve one additional card from the dealer when you choose to double down.\n")
	input("Press enter to return to where you were.\n")
	clear_screen()
	return None

def clear_screen():
	if(os.name == "nt"):
		os.system("cls") #clear screen for windows OS
	else:
		os.system("clear") #unix ftw, clear their screen differently!

def main():
	"""This is the function that sets up the game parameters and calls the play method"""
	global dealer
	try:
		money = int(input("Let's play some blackjack!  How much money would you like to play with (default is 500)?\n"))
		name = str(input("And what is your name?\n"))
		if name == "Dealer":
			print("Only the dealer can be the dealer. Please enter another name.\n")
		user = Player(name, money)
		dealer = Dealer()
		clear_screen()
		print("Thanks for playing today, " + name +"!  Let's go over a few basics:\n")
		help() #prints out some information for the user.
		while (user.money > 0):
			play_hand(user, dealer) #play hands until the user runs out of money.
		print("Thanks for playing!")
		return None
	except ValueError:
		print ("Please enter a number.\n")
		main() #give the user another opportunity to enter an amount



#Allows app to be launched directly from the command line.
if __name__ == "__main__": 
	main()