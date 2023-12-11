import pygame

import simulator
from simulator import main
from utils import Button

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
buttons = pygame.Surface((WIDTH, HEIGHT))
simulator.win = win

start_img = pygame.transform.scale(pygame.image.load("start.png"), (200, 100))
quit_img = pygame.transform.scale(pygame.image.load("quit.png"), (200, 100))
planet = pygame.transform.scale(pygame.image.load("jupiter.png"), (simulator.PLANET_SIZE * 2, simulator.PLANET_SIZE * 2))

start_button = Button(WIDTH/2, 150, start_img)
quit_button = Button(WIDTH/2, 450, quit_img)
planet = simulator.Planet(WIDTH/2, HEIGHT/2, simulator.PLANET_MASS, buttons)

running = True

while running:
    win.fill((0, 0, 0))
    start_button.draw(buttons)
    quit_button.draw(buttons)
    planet.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                main()
            if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                running = False

    if start_button.collision():
        main()
    if quit_button.collision():
        running = False
    win.blit(buttons, (0, 0))

    pygame.display.update()
