import subprocess
from sys import stdout

err = "-----------"

f = open("orig.py", "r")
newFile = f.read().split("\n")
f.close()

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
	print("|", end="")
	stdout.flush()
	# 3. Find out what line the error is on.
	try:
		lineno = err.rfind("line")
		lineno = err[lineno + 5:]
		endpos = [lineno.find("\n"), lineno.find(",")]
		try: endpos.remove(-1)
		except: pass
		endpos = min(endpos)
		lineno = lineno[:endpos]
		if lineno == "":
			# There are no errors!!! :)
			print("\n\nDone!")
			exit()
		lineno = int(lineno)
		if len(newFile) < lineno: lineno = len(newFile)
	except:
		lineno = len(newFile) # REMOVE MORE THINGS! :P
	# 4. Remove the line from the file.
	newFile.pop(lineno - 1)
