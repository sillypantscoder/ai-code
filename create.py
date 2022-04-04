import markov
import os

x = (markov.WordMarkovChain if "WORD" in os.environ and os.environ["WORD"] else markov.MarkovChain)()

files = os.listdir("test_files")
for filename in files:
	f = open("test_files/" + filename, "r")
	x.trainWith(f.read())
	f.close()

t = x.beginGeneratingText().predict(2000 if "WORD" in os.environ and os.environ["WORD"] else 20000)

f = open("orig.py", "w")
f.write(t)
f.close()
