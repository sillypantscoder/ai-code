from getch import getch
from sys import stdout
from markov import WordMarkovChain, MarkovChain
import os

def addSuggestion(s):
	print(u"\u001b[30;1m" + s.replace("\n", "↲").replace("\t", "↦") + u"\u001b[0m\u001b[" + str(len(s)) + "D", end="")

# Train the Markov chain.
x = (WordMarkovChain if "WORD" in os.environ and os.environ["WORD"] else MarkovChain)()
files = os.listdir("test_files")
for filename in files:
	f = open("test_files/" + filename, "r")
	x.trainWith(f.read())
	f.close()

text = ""
suggestion = ""
while True:
	newChar = getch()
	# Reverse the lines so we are up at the first line again.
	for i in range(text.count("\n")):
		print(u"\r\u001b[2K\u001b[1A", end="")
	print("\r\u001b[2K", end="")
	# If the user pressed a key, add it to the text.
	if newChar == '\x7f':
		# Backspace
		text = text[:-1]
	elif newChar == '\x03':
		# Ctrl-C
		exit()
	elif newChar == '\t':
		# Tab
		text += suggestion
	elif newChar == '\x1b':
		# Some modifier key
		getch()
		m = getch()
		if m == "Z":
			# Shift+Tab
			text += "\t"
	elif newChar == '\r':
		# Enter
		text += "\n"
	else:
		# Normal character
		text += newChar
	# Print what they have typed so far.
	print(text, end="")
	# Find a new suggestion.
	suggestion = x.generateFromPrevious(text)
	# Print the suggestion.
	addSuggestion(suggestion)
	# And flush STDOUT.
	stdout.flush()