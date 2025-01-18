from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption = 'Shooter game'
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

score = 0
lost = 0
life = 3

font.init()
font2 = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, asteroid=False):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.asteroid = asteroid
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            if self.asteroid == False: 
                lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



ship = Player('rocket.png', 5, win_height - 100, 80, 100, 9)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

run = True
finish = False

bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30, win_width -80), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

clock = time.Clock()

font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0 ,0))

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if mouse.get_pressed()[0]:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if finish != True:
        window.blit(background, (0,0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time <3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        sprite.groupcollide(asteroids, bullets, False, True)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, True):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            life -= 1

        if sprite.spritecollide(ship, asteroids, True):
            asteroid = Enemy('asteroid.png', randint(30, win_width -80), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
            life -= 1


        if lost >= 3 or life < 1:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        text_life = font2.render("Life: " + str(life), 1, (0, 255, 0))
        window.blit(text_life, (win_width - 80, 20)) 

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    display.update()
    time.delay(50)