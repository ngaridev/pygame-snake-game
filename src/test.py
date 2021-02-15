import pygame
from src.values import *
pygame.init()

h, w = 500, 500
timer = 30
day_number = 0

window = pygame.display.set_mode([h, w])
font_used = pygame.font.Font('freesansbold.ttf', 32)

text = font_used.render("Timer : " + str(timer) , True, black, white)
day_text = font_used.render("Day : " + str(day_number), True, black, white)

text_rect = text.get_rect()
day_text_rect = day_text.get_rect()

text_rect.center = (h // 2, w // 2)
day_text_rect.center = (h // 3, w // 3)

while timer >= 0:

    window.fill(WHITE)
    pygame.time.delay(1000)

    text = font_used.render("Timer : " + str(timer), True, BLACK, WHITE)
    day_text = font_used.render("Day : " + str(day_number), True, black, WHITE)

    if timer == 0:
        day_number += 1
        timer = 30
    timer -= 1
    window.blit(text, text_rect)
    window.blit(day_text, day_text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()