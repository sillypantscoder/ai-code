import pygame
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 10)
pygametext = ""
def py_print(s):
	global pygametext
	pygametext += str(s).replace("\t", "    ") + "\n"
def render_all_text():
	lines = pygametext.split("\n")
	rendered = []
	for t in lines:
		if len(t):
			color = 255 * (t[0] == ">")
			if color == 255 or show_other:
				if not show_other: rendered.append(FONT.render(t[2:], True, (0, 0, 0)))
				else: rendered.append(FONT.render(t[2:], True, (255 - color, color, 0)))
	widths = list(map(lambda x: x.get_width(), rendered))
	maxwidth = max(*widths)
	height = FONT.render("0", True, (0, 0, 0)).get_width() * len(rendered)
	result = pygame.Surface((maxwidth, height))
	result.fill((255, 255, 255))
	cum_y = 0
	for r in rendered:
		result.blit(r, (0, cum_y))
		cum_y += r.get_height()
	return result

f = open("orig.py", "r")
orig = f.read().split("\n")
f.close()

f = open("done.py", "r")
done = f.read().split("\n")
f.close()

donelineno = 0
lineno = 0
while donelineno < len(done):
	o = orig[lineno]
	if done[donelineno] == o:
		py_print("> " + o)
		donelineno += 1
	else:
		py_print("  " + o)
	lineno += 1
while lineno < len(orig):
	o = orig[lineno]
	py_print("  " + o)
	lineno += 1

show_other = True

screen = pygame.display.set_mode(render_all_text().get_size())

running = True
c = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONUP:
			show_other = not show_other
			screen = pygame.display.set_mode(render_all_text().get_size())
	screen.fill((100, 100, 100))
	screen.blit(render_all_text(), (0, 0))
	pygame.display.flip()
	c.tick(60)