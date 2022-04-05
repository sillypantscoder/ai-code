from getch import getch
from sys import stdout
from markov import *
import os

def addSuggestion(s):
	print(u"\u001b[34m" + s.replace("\n", "↲").replace("\t", "↦") + u"\u001b[0m\u001b[" + str(len(s)) + "D", end="")

# Train the Markov chain.
x = (WordMarkovChain if "WORD" in os.environ and os.environ["WORD"] else MarkovChain)("STRICT" in os.environ and os.environ["STRICT"])
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
	newSuggestion = True
	if newChar == '\x7f':
		# Backspace
		text = text[:-1]
	elif newChar == '\x03':
		# Ctrl-C
		print(text)
		exit()
	elif newChar == '\x1a':
		# Ctrl-Z
		# Generate a new suggestion.
		prev = suggestion
		tries = 0
		x.strict = False
		while suggestion == prev and tries < 10000:
			suggestion = x.generateFromPrevious(text)
			tries += 1
		x.strict = ("STRICT" in os.environ and os.environ["STRICT"])
		newSuggestion = False # so we can generate our own new suggestion.
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
	# Print what they have typed so far, highlighting last word.
	if len(words(text)):
		w = len(words(text)[-1])
		print(text[:-w], end=u"\u001b[31m")
		print(text[-w:], end=u"\u001b[0m")
	# Find a new suggestion.
	if newSuggestion: suggestion = x.generateFromPrevious(text)
	# Print the suggestion.
	if suggestion:
		addSuggestion(suggestion)
	# And flush STDOUT.
	stdout.flush()
