import subprocess
from sys import stdout
import selector

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
	searchcharno = len(err)
	while searchcharno > 0:
		lineno = err.rfind("line", 0, searchcharno)
		lineno = err[lineno + 5:]
		endpos = [lineno.find("\n"), lineno.find(",")] # Find the end of the line number: either a newline or a comma.
		try: endpos.remove(-1) # Remove the -1 if we couldn't find one of those.
		except: pass
		endpos = min(endpos) # Find the end index.
		lineno = lineno[:endpos] # This should be the line number.
		if lineno == "":
			# There are no errors!!! :)
			exit()
		if lineno.isdigit():
			lineno = int(lineno)
			if (lineno - 2) < len(err): break;
		searchcharno -= 1
	# 4. Remove the line from the file and update the screen.
	g.send(f"Running file... (line {lineno}/{len(newFile)}; {round((lineno / len(newFile)) * 100)}% done)")
	newFile.pop(lineno - 1)
