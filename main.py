import pygame
from constants import *
from logger import log_state
from player import Player
import circleshape
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
import sys
from shot import Shot

def main():

	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	font = pygame.font.SysFont("Arial", 30)
	HIGH_SCORE_FILE = 'highscores.txt'
	high_score = 0

	try:
		with open(HIGH_SCORE_FILE, "r") as f:
			high_score = int(f.read())
	except (FileNotFoundError, ValueError):
		high_score = 0
		with open(HIGH_SCORE_FILE, "w") as f:
			f.write(str(high_score))


	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Asteroid.containers = (asteroids, updatable, drawable)
	Player.containers = (updatable, drawable)
	AsteroidField.containers = (updatable,)
	Shot.containers = (shots,updatable,drawable)
	game_clock = pygame.time.Clock()
	dt = 0
	player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	AsteroidField1 = AsteroidField()
	#print("Updatable:", updatable)
	#print("Drawable:", drawable)

	while True:
		log_state()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		screen.fill("black")
		updatable.update(dt)

		for collision in asteroids:
			if collision.collides_with(player1):
				player1.death()
				if player1.lives < 1:
					log_event("player_hit")
					print("Game over!")
					if player1.score > high_score:
						high_score = player1.score
						with open(HIGH_SCORE_FILE, "w") as f:
							f.write(str(high_score))
					sys.exit()
			for shot in shots:
				if collision.collides_with(shot):
					log_event("asteroid_shot")
					collision.split()
					player1.scoring(collision.points)
					shot.kill()

		for drawing in drawable:
			drawing.draw(screen)
		
		score_current = font.render(f"Score: {player1.score}", True, "white")
		score_high = font.render(f"High Score: {high_score}", True, "white")

		screen.blit(score_current, (10, 10))
		screen.blit(score_high, (300, 10))
		pygame.display.flip()
		dt = game_clock.tick(60) / 1000
		#print(dt)
            
      


if __name__ == "__main__":
    main()
