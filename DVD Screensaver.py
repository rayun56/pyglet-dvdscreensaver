import pygame
import random
import time
import screeninfo
import humanize

deadzone = 20 / 1000  # 20 milliseconds


size = width, height = (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DVD Screensaver")

dvds = [pygame.image.load("Images\dvdlogo-0" + str(x) + ".png") for x in range(5)]
dvdrect = dvds[0].get_rect()
dvdrect.x = width / 2 + random.randint(0, 100)
dvdrect.y = height / 2 + random.randint(0, 100)

corner_cunter = 0
time_since = None
vertical_hit = 1
horizontal_hit = 1
dvd_i = 0
last_hit = None

pygame.init()
run = True

while run:
    pygame.time.delay(6)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False
    dvdrect = dvdrect.move(speed)
    if dvdrect.left < -24 or dvdrect.right > width + 24:
        speed[0] = -1 * speed[0]
        horizontal_hit = time.time()
        temp_i = dvd_i
        while dvd_i == temp_i:
            dvd_i = random.randint(0, 4)
    if dvdrect.top < -24 or dvdrect.bottom > height + 24:
        speed[1] = -1 * speed[1]
        vertical_hit = time.time()
        temp_i = dvd_i
        while dvd_i == temp_i:
            dvd_i = random.randint(0, 4)
    try:
        if time.time() - horizontal_hit <= deadzone and time.time() - vertical_hit <= deadzone and (time.time() - time_since >= 2):
            corner_cunter += 1
            time_since = time.time()
    except TypeError:
        if time.time() - horizontal_hit <= deadzone and time.time() - vertical_hit <= deadzone:
            corner_cunter += 1
            time_since = time.time()

    counter_text = pygame.font.SysFont("Calibri", 80, True).render("Corner Hits: "+str(corner_cunter), True, (255, 255, 255))
    if corner_cunter > 0:
        last_hit = time.time() - time_since
    time_text = pygame.font.SysFont("Calibri", 40, True).render("Time since last hit: " + humanize.naturaldelta(last_hit), True, (255, 255, 255))
    screen.fill(black)
    screen.blit(dvds[dvd_i], dvdrect)
    screen.blit(counter_text, (width / 2 - counter_text.get_size()[0] / 2, 10))
    screen.blit(time_text, (width / 2 - time_text.get_size()[0] / 2, 80))
    pygame.display.update()