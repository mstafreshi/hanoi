""" The tower of Hanoi 
	_________________________________________________
	Sorry for my bad english!
	Writted with python and pygame module.
	Note : this program initially find a list of movements 
	for the problem and then moves the disk in order of the list
	of solution . Therefore you must execute the program
	with a suitable n disk.
	If we had n disks, the movements for solving the problem is
	(2 ^ n) - 1 .
	I advice you that you examine the program with maximum 
	of n = 15 .
	_________________________________________________
 
	Programmer	: Mohsen Safari
	Email		: safari.tafreshi@gmail.com
	Website		: safarionline.ir
"""
 
import pygame, sys, inspect
 
# Number of the disk in tower of hanoi
N = 5
 
# Number of ticks in one second
FREQ = 500
 
# If user has provided disk number in command line use it
if len(sys.argv) == 2 and int(sys.argv[1]) > 3:
	N = int(sys.argv[1])
	if N > 16:
		print("Number of disk is too high.")
		print("If you are sure change code in line 31")
		sys.exit(1)
 
 
pygame.init()
 
BGCOLOR		   = (209, 209, 209)
BARSCOLOR	   = (  0, 104, 139)
DISKSCOLOR	   = (205,  51,  51)
MOVEFONTCOLOR  = (255,   0, 255)
TITLEFONTCOLOR = (255,  64,   0)
 
SIZE = WIDTH, HEIGHT = (540, 350)
 
# A counter for counting number of disk moves.
number_of_moves = 0
 
BASICFONT  = pygame.font.SysFont("freesansbold", 20)
BIGFONT	   = pygame.font.SysFont("freesansbold", 42)
 
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tower of Hanoi")
 
clock = pygame.time.Clock()
 
# Movements! in this list we store the moves of the disks
m = [] 
 
# horizonatl bar height and disk height
HBH = DH = 10
 
# Distance between two disk
DBD = 15
 
# Static elements: the 3 vertical bars and one horizental bar
S = [0, 0, 0, 0]
 
# s[3] is the horizontal bar
S[3] = pygame.Rect(20, HEIGHT - 20, WIDTH - 40, HBH)
 
# s[0] and s[1] and s[2] are the vertical bars 
for i in range(0, 3):
	S[i] = pygame.Rect(WIDTH / 3 * (i + 1) - 100, 100 , 10, S[3].top - 100)
 
# active_elements! each sublist show the disks in the corresponding bar
a = [ [], [], [] ]
 
 
# Adding all disks to a[0]
# For a[0] top offset the largest disk in first vertical bar(=S[0])
# is the top offset of the horizental bar(=S[3])
top =S[3].top - HBH 
 
# First disk width
dw = 150
 
# Reduce disk width.
# Next disk width must be "rdw" smaller than this disk
rdw = 30
 
while dw / N <= rdw :
	rdw = rdw - 1
	continue
 
for i in range(N) :
	a[0].append(pygame.Rect(S[0].centerx - dw / 2, top - HBH , dw, DH))
	top = top - DH - 5
	dw = dw - rdw
# end of the initial positioning!
 
 
# Show all elements on the screen.
# The content of the lists bellow are Rect and have
# their coordiantes and width and height 
# We simply show them on the screen.
def update_screen() :
	# check event queue for pygame.QUIT event!
	check_events()
 
	SCREEN.fill(BGCOLOR)
	for i in range(len(S)) :
		pygame.draw.rect(SCREEN, BARSCOLOR, S[i], 0)
 
	for i in range(len(a)) :
		for j in range(len(a[i])) :
			pygame.draw.rect(SCREEN, DISKSCOLOR, a[i][j], 0)
 
	# Print Number of moves on screen
	text = "Moves: {0}".format(number_of_moves)
	surf = BASICFONT.render(text, True, MOVEFONTCOLOR)
	rect = surf.get_rect()
	rect.topleft = (WIDTH - rect.width - 10, 0)
	SCREEN.blit(surf, rect)
 
	# Print Title of program on screen
	surf = BIGFONT.render("Tower of Hanoi", True, TITLEFONTCOLOR)
	rect = surf.get_rect()
	rect.center = (S[1].left, 30)
	SCREEN.blit(surf, rect)
 
	pygame.display.update()
 
 
def move() :
	# Note that in this place hanoi towers movements are completely calculated!
	# and these movements are stored in list "m".
	# Now we take each move and then move the disk to its destination bar.
	# Also note that in this function we only change the positions of
	# the disk in the screen and then call the update_screen function.
	# "update_screen" function show all elements on 
	# screen. all elements are lists: S and a
 
	# A counter for counting number of disk moves.
	global number_of_moves
 
	for i in range(len(m)) :
		# m[i][0] is starting bar and i is a number in (0,1,2)	
		init = m[i][0]
 
		# m[i][1] is the destination bar and i is a number(0,1,2)
		dest = m[i][1]
 
		if len(a[dest]) != 0:
			dest_y = a[dest][-1].top - DBD # DBD: distance between disks
		else :
			dest_y = S[3].top - HBH # HBH: horizontal bar height 
 
		# moves the disk to the top of the its bar!
		while a[init][-1].top > S[init].top - 30:
			clock.tick(FREQ)
			a[init][-1].move_ip([0, -1])
			update_screen()
 
		# Destination bar is at left of current bar or right of it????
		if a[init][-1].centerx < S[dest].centerx:
			# Destination bar is at right of current bar
			while a[init][-1].centerx < S[dest].centerx:
				clock.tick(FREQ)
				a[init][-1].move_ip([1,0])
				update_screen()
		else:
			# Destination bar is at the left of current bar
			while a[init][-1].centerx > S[dest].centerx:
				clock.tick(FREQ)
				a[init][-1].move_ip([-1,0])
				update_screen()
 
		# Move disk down in the destination bar
		while a[init][-1].centery < dest_y :
			clock.tick(FREQ)
			a[init][-1].move_ip([0, 1])
			update_screen()
 
		# Remove the moved disk from the its location
		# in bar "init" and add it to the dest bar
		a[dest].append(a[init].pop())		
		number_of_moves += 1		
 
# The hanoi towers function itself!
# All moves of the disks will be stored in the list 'm'
def hanoi(n, b0, b1, b2) :
	if n == 1 :
		# Store the move in the list m
		m.append([b0, b2])
	else :
		hanoi(n - 1, b0, b2, b1)
		# Store the move in the list m
		m.append([b0, b2])
		hanoi(n - 1, b1, b0, b2)
 
# Function for exit from the application
def check_events() :
	# Exit with click on close button
	for event in pygame.event.get() :
		if event.type == pygame.QUIT:
			sys.exit()
 
		# Exit with "Escape" button or "q" button
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				sys.exit()
 
# Info about this program
def print_program_info():
	print("Hanoi towers with pygame")
	print("------------------------")
	print("Programmer	: Mohsen Safari")
	print("Website		: safarionline.ir")	
 
 
if __name__ == "__main__":
	# print information on console about this program
	print_program_info()
 
	# move hanoi towers program
	hanoi(N, 0,1, 2)
 
	# Now hanoi profram is solved. All the moves are in "m" variable
	# "m" means "moves"! In function we move all disks to its destination
	move()
 
	# Program is done. wait for quit event.
	while 1 :
		check_events()
