#Author: Rojit Ghimire

import requests 
from bs4 import BeautifulSoup
from csv import writer
from random import choice
from csv import DictReader

base_url = "http://quotes.toscrape.com"

def read_quotes(filename):
	with open(filename, "r",encoding="utf-8") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

read_quotes("quotes.csv")

def start_game(quotes):
	quote = choice(quotes)
	remaining_guesses = 4
	print(quote["text"])

	guess = ''

	while guess.lower() != quote["author"].lower() and remaining_guesses > 0 :
		guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} \n")
		if guess == quote["author"].lower():
			print("YOU GOT IT RIGHT.YEEHAW")
			break
		
		remaining_guesses -= 1
		if remaining_guesses == 3:
			response = requests.get(f"{base_url}{quote['bio-link']}")
			soup = BeautifulSoup(response.text, "html.parser")
			birth_date = soup.find(class_="author-born-date").get_text()
			birth_place = soup.find(class_ = "author-born-location").get_text()
			print(f"HERE IS A HINT.The author was born on {birth_date} in {birth_place}.")
		
		elif remaining_guesses == 2:
			a = quote["author"][0]
			print(f"HERE IS A HINT. The author first name start with {a}.")
		
		elif remaining_guesses == 1:
			last_initial = quote["author"].split(" ")[1][0]
			print(f"The author last name starts with {last_initial}")
		
		else:
			print(f"You ran out of guesses. The answer was {quote['author']}")

	again = ''
	
	while again.lower() not in('y','yes','n','no'):
		again = input("Would you like to play again(y/n)?")

	if again.lower() in ('yes','y'):
		return start_game()
	else:
		print("THANKS FOR PLAYING...GOODBYE")

quotes = read_quotes("quotes.csv")
start_game(quotes)
