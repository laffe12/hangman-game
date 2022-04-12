import pygame
import math
import random

# initialize pygame and setup display window
pygame.init() 
WIDTH, HEIGHT = 800, 500 
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman!")

# fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 75)

# load images
images = []
for i in range(7):
	image = pygame.image.load("images/hangman" + str(i) + ".png")
	images.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65

# calculate distance between letters
for i in range(26):
	x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
	y = start_y + ((i // 13) * (GAP + RADIUS * 2))
	letters.append([x, y, chr(A + i), True])

# game variables
hangman_status = 0 		# used for adding more limbs
words = ["ELEPHANT", "PYTHON", "SNAKE", "BIRD", "ORANGUTANG", "DOLPHIN"]
word = random.choice(words)	# random picks a word from words list
guessed_words = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 102, 51)
def draw():
	win.fill(GREEN)
	text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
	win.blit(text, ((WIDTH - text.get_width())/2, 20))

	# draw word
	display_word = ""
	for letter in word:
		if letter in guessed_words:
			display_word += letter + " "
		else:
			display_word += "_ "
	text = WORD_FONT.render(display_word, 1, BLACK)
	win.blit(text, (400,200))
	
	# draw buttons
	for letter in letters:
		x, y, ltr, visible = letter
		if visible:
			pygame.draw.circle(win, BLACK, (x, y), RADIUS, 2)
			text = LETTER_FONT.render(ltr, 1, BLACK)
			win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
			

	win.blit(images[hangman_status], (150, 100)) # draw image on window
	pygame.display.update()						 # update display

def display_message(message):
		win.fill(GREEN)
		text = WORD_FONT.render(message, 1, BLACK)
		win.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
		pygame.display.update()
		pygame.time.delay(3000)

def main():
	# setup game loop
	global hangman_status
	run = True
	FPS = 60
	clock = pygame.time.Clock() # keeps track of game time / speed
	
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# quits the game and closes the window
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				m_x, m_y = pygame.mouse.get_pos()	# get the coordinates for mousebutton press
				for letter in letters:
					x, y, ltr, visible = letter
					if visible:
						dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
						if dis < RADIUS:
							letter[3] = False
							guessed_words.append(ltr)
							if ltr not in word:
								hangman_status += 1

		draw()

		won = True
		for letter in word:
			if letter not in guessed_words:
				won = False
				break
		if won:
			display_message("YOU SHALL LIVE")
			break

		if hangman_status == 6:
			display_message("YOU'RE DEAD!")
			break


main()
pygame.quit()