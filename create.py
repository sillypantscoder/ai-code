import markov
import os
import selector

iters = 20000

running = True
while running:
	choice = selector.selector("Create File", ["", "-Least coherent-", "", ">>> Character Mode", ">>> Phrase Mode", ">>> Word Mode", ">>> Line Mode", "", "-Most coherent-"])
	if choice == 3:
		running = False
		x = markov.MarkovChain()
	elif choice == 4:
		running = False
		x = markov.WordMarkovChain()
		iters = 7000
	elif choice == 5:
		running = False
		x = markov.WordMarkovChain([" ", "\n", "\t", ",", ".", "(", ")", "!", "?", "\"", "'", ":", ";", "-", "/", "\\", "+", "-"])
		iters = 5000
	elif choice == 6:
		running = False
		x = markov.WordMarkovChain(["\n"])
		iters = 1000
	elif choice == -1:
		exit()

g = selector.progress("Generating file...")
g.send(None)

files = os.listdir("test_files")
for filename in files:
	f = open("test_files/" + filename, "r")
	x.trainWith(f.read())
	f.close()

t = x.beginGeneratingText()
for i in range(iters):
	t.predict(1)
	g.send(f"Generating file... ({round((i / iters) * 100)}% done)")

f = open("orig.py", "w")
f.write(t.value)
f.close()
