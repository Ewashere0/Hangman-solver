#add any global variables your AI needs here:

#wordlist is all possible words the game could pick as a puzzle
#it is only initialized when your module is imported, so do not change it
wordlist = []

#all words that are possible after certain variables are known such as letters
possibleWords = []

#letters is a list of all characters your program could guess
#it is re-initialized each round, so you can modify it
letters = []

#the number of words that contain the 'i'th' letter
lettersOccurrences = []

#all guesses this round
guessed = []

#current guess
guess = ""


filein = open("base-words.txt", "r")
wordlist = filein.read().lower().split("\n")
filein.close();

#round initialization
#this is called at the start of each round
#the input string is a single _ for each character in the puzzle
def initround(string):

	possibleWords.clear()
	letters.clear()
	lettersOccurrences.clear()
	guessed.clear()

	#initializes the list of letters that could be guessed
	#you can use this list in your AI implementation if desired
	for i in range(ord('a'), ord('z')+1):
		letters.append(chr(i))
		lettersOccurrences.append(0)

	#eliminate words which have the incorrect length
	for word in wordlist:
		if len(word) == len(string):
			possibleWords.append(word)

	#add any more initialization code your AI requires here
	#...


#Add your AI code to guess a letter here
#The input string is the current puzzle, with _ for any unguessed letters
#You should output one lower-case character
def makeguess(string):

	for i in range(len(possibleWords) - 1, -1, -1):
		broken = False

		#If a letter is guessed incorrectly, words containing that letter are removed
		#(ex. Puzzle: ______, guessed: [e], possibleWords: 'person' is removed)
		for j, letter in enumerate(guessed):
			if letter not in string and letter in possibleWords[i]:
				possibleWords.pop(i)
				broken = True
				break
		if broken:
			continue

		#Eliminate words which have duplicate solved letters in an incorrect location
		#(ex. Puzzle: _o_____oo_, possibleWords: 'trochozoon' is removed)
		for j, letter in enumerate(possibleWords[i]):
			if letter in string and list(string)[j] != letter:
				possibleWords.pop(i)
				broken = True
				break
		if broken:
			continue

		#Eliminate words which dont contain newly solved letters
		#ex: Puzzle: ______e_s, possibleWords: 'voyageur' is removed
		for j, letter in enumerate(string):
			if letter != "_":
				if possibleWords[i].find(letter, j) != j:
					possibleWords.pop(i)
					break

	#Find the letter which appears in the most words, in locations which have not yet been guessed.
	#This is better than the letter which appears most often because
	#this will not be effected by multiple of the same letter in one word
	#(ex: PossibleWords: 'subbookkeeper', lettersOccurrences: b = 1, e = 1, k = 1, o = 1, p = 1, r = 1, s = 1, u = 1)
	for i in range(len(letters)):
		lettersOccurrences[i] = 0

	for word in possibleWords:
		for i, letter in enumerate(string):
			if letter != "_":
				word = word[:i] + '_' + word[i+1:]
		for i, letter in enumerate(letters):
			if letter in word:
				lettersOccurrences[i] += 1

	#Guess the most common letter that hasn't already been guessed
	greatestOccurrence = 0
	for i, occurrence in enumerate(lettersOccurrences):
		if occurrence > greatestOccurrence and chr(i + ord("a")) not in guessed:
			greatestOccurrence = occurrence
			guess = chr(i + ord("a"))
	guessed.append(guess)
	# print(possibleWords)
	return(guess)
