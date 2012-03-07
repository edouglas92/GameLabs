import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

def load_sound(sound_name):
	try:
		sound = pygame.mixer.Sound(sound_name)
	except pygame.error, message:
		print "Cannot load sound: " + sound_name
		raise SystemExit, message
	return sound

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect1 = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_rect2 = pygame.Rect((SCREEN_WIDTH - PADDLE_START_X, SCREEN_HEIGHT - PADDLE_HEIGHT), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score1 = 0
score2 = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

screen_id = 0

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect1.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect1.top < 0:
				paddle_rect1.top = 0
			elif paddle_rect1.bottom >= SCREEN_HEIGHT:
				paddle_rect1.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect1.top > 0:
		paddle_rect1.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect1.bottom < SCREEN_HEIGHT:
		paddle_rect1.top += BALL_SPEED
		
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	if screen_id == 1 and pygame.key.get_pressed()[pygame.K_y]:
		score1 = 0
		score2 = 0
		screen_id = 0
	if screen_id == 1 and pygame.key.get_pressed()[pygame.K_n]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]
	
	if ball_rect.top < paddle_rect2.top and paddle_rect2.top > 0:
		paddle_rect2.top -= BALL_SPEED - 1
	elif ball_rect.top > paddle_rect2.top and paddle_rect2.bottom < SCREEN_HEIGHT:
		paddle_rect2.top += BALL_SPEED - 1

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if ball_rect.right >= SCREEN_WIDTH + 50:
		ball_speed[0] = -ball_speed[0]
		score1 += 1
		ball_rect.left = SCREEN_WIDTH / 2
		ball_rect.top = SCREEN_HEIGHT / 2
		ball_speed[0] = -ball_speed[0]
		pygame.time.delay(350)
	if ball_rect.left <= 0 - 50:
		ball_speed[0] = -ball_speed[0]
		score2 += 1
		ball_rect.left = SCREEN_WIDTH / 2
		ball_rect.top = SCREEN_HEIGHT / 2
		ball_speed[0] = -ball_speed[0]
		pygame.time.delay(350)

	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect1.colliderect(ball_rect) or paddle_rect2.colliderect(ball_rect):
		bong = load_sound('p_hit.wav')
		bong.play()
		ball_speed[0] = -ball_speed[0]
		
	if score1 == 11 or score2 == 11:
		screen_id = 1
	
	# Clear screen
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH / 2 - 10, 0, 10, SCREEN_HEIGHT))
	
	score_text1 = font.render(str(score1), True, (0, 255, 0))
	score_text2 = font.render(str(score2), True, (0, 255, 0))
	screen.blit(score_text1, ((SCREEN_WIDTH / 4) - font.size(str(score1))[0] / 2, 5))
	screen.blit(score_text2, ((SCREEN_WIDTH - (SCREEN_WIDTH / 4) - font.size(str(score1))[0] / 2, 5)))
	
	if screen_id == 0:
	# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (0, 255, 0), paddle_rect1) # Your paddle
		pygame.draw.rect(screen, (0, 255, 0), paddle_rect2)
		pygame.draw.circle(screen, (0, 255, 0), ball_rect.center, ball_rect.width / 2)

	elif screen_id == 1 and score1 == 11:
		game_over = font.render("GAME OVER", True, (0, 255, 0))
		screen.blit(game_over, ((SCREEN_WIDTH / 6), (SCREEN_HEIGHT / 2.5)))
		restart = font.render("YOU WIN! Restart? (y/n)", True, (0, 255, 0))
		screen.blit(restart, ((SCREEN_WIDTH / 6 - 40), (SCREEN_HEIGHT / 2.5 + 25)))
		ball_rect.left = SCREEN_WIDTH / 2
		ball_rect.top = SCREEN_HEIGHT / 2
	else:
		game_over = font.render("GAME OVER", True, (0, 255, 0))
		screen.blit(game_over, ((SCREEN_WIDTH - SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 2.5)))
		restart = font.render("COMPUTER WINS! Restart? (y/n)", True, (0, 255, 0))
		screen.blit(restart, ((SCREEN_WIDTH - SCREEN_WIDTH / 2.25), (SCREEN_HEIGHT / 2.5 + 25)))
		ball_rect.left = SCREEN_WIDTH / 2
		ball_rect.top = SCREEN_HEIGHT / 2
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)

