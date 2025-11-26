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
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	wrapable = pygame.sprite.Group()

	Asteroid.containers = (asteroids, updatable, drawable)
	Player.containers = (wrapable, updatable, drawable)
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
		right_edge = SCREEN_WIDTH
		left_edge = 0
		top_edge = SCREEN_HEIGHT
		bottom_edge = 0
		print(player1.position.y)
		for wrap in wrapable:
			if wrap.position.x > right_edge:
				wrap.position.x = left_edge +1
			if wrap.position.x < left_edge:
				wrap.position.x = right_edge +1
			if wrap.position.y > top_edge:
				wrap.position.y = bottom_edge +1
			if wrap.position.y < bottom_edge:
				wrap.position.y = top_edge +1

		for collision in asteroids:
			if collision.collides_with(player1):
				log_event("player_hit")
				print("Game over!")
				sys.exit()
			for shot in shots:
				if collision.collides_with(shot):
					log_event("asteroid_shot")
					collision.split()
					shot.kill()

		for drawing in drawable:
			drawing.draw(screen)
		
		pygame.display.flip()
		dt = game_clock.tick(60) / 1000
		#print(dt)
            
      


if __name__ == "__main__":
    main()
