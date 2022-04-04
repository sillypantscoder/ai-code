from random import choice

class MarkovChain:
	def __init__(self):
		self.dir: dict[str, list[str]] = {}
		self.start: list[str] = []
	def recordSingle(self, before, after):
		if before not in self.dir: self.dir[before] = []
		self.dir[before].append(after)
	def trainWith(self, text):
		if not text: return;
		self.start.append(text[0])
		for i in range(len(text) - 1):
			self.recordSingle(text[i], text[i + 1])
	def predictNextChar(self, before):
		if before not in self.dir: return "";
		if len(self.dir[before]) == 0: return "";
		return choice(self.dir[before])
	def generateFromPrevious(self, before):
		if len(before) == 0: return "";
		last = before[-1]
		return self.predictNextChar(last)
	def beginGeneratingText(self):
		return GenerationProgress(choice(self.start), self)

def words(s: str):
	r = []
	p = ""
	for c in s:
		p += c
		if c in [" ", "\n", "\t"]:
			r.append(p)
			p = ""
	if len(p) > 0: r.append(p)
	return r

class WordMarkovChain(MarkovChain):
	def trainWith(self, text: str):
		if not text: return;
		s = words(text)
		self.start.append(s[0])
		for i in range(len(s) - 1):
			self.recordSingle(s[i], s[i + 1])
	def generateFromPrevious(self, before):
		last = words(before)[-1]
		return self.predictNextChar(last)

class GenerationProgress:
	def __init__(self, start, o):
		self.fromObj = o
		self.value = start
	def predict(self, iters):
		for i in range(iters): self.value += self.fromObj.generateFromPrevious(self.value)
		return self.value
