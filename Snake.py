# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:01:35 2020

@author: jbris
"""
import datetime
import pygame
import random

class body():
    def __init__(self,x,y):
        self.x=x
        self.y=y

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

#pygame.display.update()

background = pygame.image.load('background.png')

randx = range(20,790,10)
randy = range(20,590,10)
food = pygame.image.load('apple.png')
foodx = random.choice(randx)
foody = random.choice(randy)
eat = False

# Head
#snake
segments = []
for i in range(3):
    segments.append(body(400,300+i*20))

def blit(image,x,y):
    screen.blit(image,(x,y))
    
direct = "" 

speed = 10
score = 0 
font = pygame.font.SysFont(None, 72)
wait = 0
upped = True

is_running = True
while is_running:
    clock.tick(speed)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        direct = "right"
    if keys[pygame.K_LEFT]:
        direct = "left"
    if keys[pygame.K_DOWN]:
        direct = "down"
    if keys[pygame.K_UP]:
        direct = "up"
    
    if direct=="right":
        segments.remove(segments[len(segments)-1])
        if segments[0].x >= 790:
            segments.insert(0, body(0,segments[0].y))
        else:
            segments.insert(0, body(segments[0].x+22,segments[0].y))
    elif direct == "left":
        segments.remove(segments[len(segments)-1])
        if segments[0].x <= 10:
            segments.insert(0, body(800,segments[0].y))
        else:
            segments.insert(0, body(segments[0].x-22,segments[0].y))
    elif direct == "up":
        segments.remove(segments[len(segments)-1])
        if segments[0].y <= 10:
            segments.insert(0, body(segments[0].x, 590))
        else:
            newhead = [body(segments[0].x ,segments[0].y-22)]
            segments = newhead+segments
    else:
        segments.remove(segments[len(segments)-1])
        if segments[0].y >= 590:
            segments.insert(0, body(segments[0].x, 0))
        else:
            segments.insert(0, body(segments[0].x,segments[0].y + 22))
    
    if abs(segments[0].x-foodx-5)<20 and abs(segments[0].y-foody-5)<20:
        eat = True
    
    if eat:
        score += 1
        foodx = random.choice(randx)
        foody = random.choice(randy)
        eat = False
        segments.append(body(segments[len(segments)-1].x,segments[len(segments)-1].y))
    
    if score != 0 and score % 10 == 9:
        upped = False

    if not upped:
        if score != 0 and score % 10 == 0:    
            upped = True
            if speed < 40:
                speed += 5
            wait = speed*2
            msg = font.render("Speed up", True, (0,0,0))
            wid = pygame.Surface.get_width(msg)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    for part in segments[1:]:
        if part.x == segments[0].x :
            if part.y == segments[0].y:
                is_running = False
                gameover = font.render("GAME OVER", True, (0,0,0))
                go_wid = pygame.Surface.get_width(gameover)
         
    score_img = font.render(str(score), True, (0,0,0)) 
    blit(background,0,0)
    blit(score_img, 400,50)
    if not is_running:
        blit(gameover, 400 - go_wid/2,250)
    if wait > 0:
        wait-=1
        blit(msg, 430-wid/2, 100)
    for segment in segments:
        pygame.draw.rect(screen, (0,0,0), (segment.x, segment.y, 20,20))    
    blit(food,foodx,foody)
    pygame.display.update()

pygame.quit()

datetoday = datetime.date.today()
of = open('scores.txt', 'a')
of.write('Score '+ str(score) + '     ' +datetoday.strftime('%d %b %Y') + '\n')
of.close()
