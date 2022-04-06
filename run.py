import subprocess
from sys import stdout
import selector
import re

err = "-----------"

f = open("orig.py", "r")
newFile = f.read().split("\n")
f.close()

g = selector.progress("Running file...")
g.send(None)

while len(err) > 10:
	# 1. Write the new file.
	# (Done early so that the next step will find errors.)
	f = open("done.py", "w")
	f.write("\n".join(newFile))
	f.close()
	# 2. Run the program.
	com = "python3 done.py"
	p = subprocess.Popen(com.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	err = err.decode("UTF-8")
	stdout.flush()
	# 3. Find out what line the error is on.
	x = [err[m.end()+1:] for m in re.finditer('line', err)]
	# x = ["<lineno>\n			^\nSyntaxError: blah blah blah"]
	y = []
	for i in x:
		r = ""
		for char in i:
				if char in "1234567890":
						r += char
				else: break;
		y.append(r)
	# y = possible line numbers
	lineno = None
	y.reverse()
	for l in y:
		# l = possible line number. Reversed so we get the deepest error first.
		if l.isdigit(): # needs to be a number
			lineno = int(l)
			if lineno < len(newFile): # needs to not be off the end of the file
				break;
			else: lineno = None
	# 4. Remove the line from the file and update the screen.
	if lineno == None: exit()
	g.send(f"Running file... (line {lineno}/{len(newFile)}; {round((lineno / len(newFile)) * 100)}% done)")
	newFile.pop(lineno - 1)
