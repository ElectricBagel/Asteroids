from circleshape import CircleShape
import pygame
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.lives = 3
        self.score = 0
        self.friction = 0.01
        self.acceleration = 0.05
        self.unit_vector = pygame.Vector2(0, 1)
        self.velocity = pygame.Vector2(0,0)


# in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.drift(dt)
        else:
            self.position += self.velocity * dt

        if keys[pygame.K_a]:
            self.rotate(dt *-1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, forward=True)
        if keys[pygame.K_s]:
            self.move(dt, forward=False)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
    
    def move(self, dt, forward=True):
        direction = 1 if forward else -1
        forward_vec = self.unit_vector.rotate(self.rotation)
        self.velocity += forward_vec * (PLAYER_SPEED * self.acceleration * direction)

        if self.velocity.length() > PLAYER_SPEED:
            self.velocity.scale_to_length(PLAYER_SPEED)
    
    def drift(self,dt):
        self.velocity *= (1 - self.friction)
        self.position += self.velocity * dt

    def shoot(self):
        if self.cooldown <= 0:
            new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            new_shot.rotation = self.rotation
            new_angle = pygame.Vector2(0, 1).rotate(self.rotation)
            new_shot.velocity = new_angle * PLAYER_SHOOT_SPEED
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def death(self):
        self.lives -= 1
        self.position.x = SCREEN_WIDTH / 2
        self.position.y = SCREEN_HEIGHT / 2

    def scoring(self, points):
        self.score += points



    
        
