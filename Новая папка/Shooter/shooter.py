import pygame
from random import *

screen = pygame.display.set_mode((800,600))

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('Laser.wav')
alien_explosion_sound = pygame.mixer.Sound('AlienExplosion.wav')
player_explosion_sound = pygame.mixer.Sound('ShipExplosion.wav')

pygame.font.init()
font = pygame.font.SysFont('Arial', 36)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, file, size, x, y, speed):
        super().__init__()
        self.file = pygame.image.load(file)
        self.file = pygame.transform.scale(self.file, (size, size))
        self.rect = self.file.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw(self):
        screen.blit(self.file, self.rect)
    
class Player(GameSprite):
    score = 0
    fail = 0
    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.draw()

class Alien(GameSprite):
    def move(self):
        if self.rect.y < 500:
            self.rect.y += self.speed
            self.collide()
        else:
            aliens_list.remove(self)
            player.fail += 1
        self.draw()
    def collide(self):
        if pygame.sprite.collide_rect(self, player):
            aliens_list.remove(self)
            player_explosion_sound.play()

class Bullet(GameSprite):
    def move(self):
        if self.rect.y > 100:
            self.rect.y -= self.speed
            self.collide()
        else:
            bullets_list.remove(self)
        self.draw()
    def collide(self):
        for alien in aliens_list:
            if pygame.sprite.collide_rect(self, alien):
                bullets_list.remove(self)
                aliens_list.remove(alien)
                player.score += 1
                alien_explosion_sound.play()
                

player = Player("ship.png", 40, 400, 500, 2)

aliens_list = []
for i in range(1000):
    alien = Alien("alien.png", 40, randint(100,700), -i * 40, 2)
    aliens_list.append(alien)

bullets_list = []

game = True
while game:
    screen.fill((50, 100, 100))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullet = Bullet("bullet.png",40, player.rect.x, player.rect.y, 10)
                bullets_list.append(bullet)
                fire_sound.play()
    player.control()
    for alien in aliens_list:
        alien.move()
    for bullet in bullets_list:
        bullet.move()
    counter = font.render("Осталось: " + str(len(aliens_list)), 1, (255, 255, 255))
    screen.blit(counter,(10,10))
    score = font.render("Подбито: " + str(player.score), 1, (255, 255, 255))
    screen.blit(score,(10,50))
    fail = font.render("Пропущено: " + str(player.fail), 1, (255, 255, 255))
    screen.blit(fail,(10,90))
    pygame.display.update()
    pygame.time.delay(10)

