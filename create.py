import markov
import os
import selector

running = True
while running:
	choice = selector.selector("Create File", ["", "Character Mode >", "Word Mode >"])
	if choice == 1:
		running = False
		x = markov.MarkovChain()
	elif choice == 2:
		running = False
		x = markov.WordMarkovChain()
	elif choice == -1:
		exit()

g = selector.progress("Generating file...")
g.send(None)

files = os.listdir("test_files")
for filename in files:
	f = open("test_files/" + filename, "r")
	x.trainWith(f.read())
	f.close()

iters = (5000 if isinstance(x, markov.WordMarkovChain) else 20000)
t = x.beginGeneratingText()
for i in range(iters):
	t.predict(1)
	g.send(f"Generating file... ({round((i / iters) * 100)}% done)")

f = open("orig.py", "w")
f.write(t.value)
f.close()
