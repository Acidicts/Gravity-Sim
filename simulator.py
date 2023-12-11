import pygame
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
trails = pygame.Surface((WIDTH, HEIGHT))
colours = [
    (255, 255, 255),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 128, 0),  # Dark Green
    (255, 140, 0)  # Dark Orange
]
global trail_col
global trail
trail_col = colours[0]
trail = True
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
objects = []

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))
trail_button_img = pygame.transform.scale(pygame.image.load("Trails.png"), (100, 50))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.mouse_pos = pygame.mouse.get_pos()
        self.down = False

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, surf):
        self.mouse_pos = pygame.mouse.get_pos()
        self.collision()
        self.draw(surf)

    def collision(self):
        global trail
        if self.rect.collidepoint(self.mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print("Clicked")
                    trail = not trail
                    print(trail)

            return True
        else:
            return False

class Planet:
    def __init__(self, x, y, mass, surface=win):
        self.x = x
        self.y = y
        self.mass = mass
        self.surface = surface

    def draw(self):
        self.surface.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * self.mass * planet.mass) / distance ** 2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)
        self.draw_trail()

    def draw_trail(self):
        pygame.draw.circle(trails, trail_col, (int(self.x), int(self.y)), 1)


def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / 100
    vel_y = (m_y - t_y) / 100
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj


def main():
    running = True
    clock = pygame.time.Clock()

    trails_button = Button(0, 600, trail_button_img)
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    temp_obj_pos = None

    trails.set_colorkey((0, 0, 0))

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            global trail_col
            global trail
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    trail_col = colours[0]
                if event.key == pygame.K_2:
                    trail_col = colours[1]
                if event.key == pygame.K_3:
                    trail_col = colours[2]
                if event.key == pygame.K_4:
                    trail_col = colours[3]
                if event.key == pygame.K_5:
                    trail_col = colours[4]
                if event.key == pygame.K_6:
                    trail_col = colours[5]
                if event.key == pygame.K_7:
                    trail_col = colours[6]
                if event.key == pygame.K_8:
                    trail_col = colours[7]
                if event.key == pygame.K_9:
                    trail_col = colours[8]
                if event.key == pygame.K_0:
                    trail_col = colours[9]
                if event.key == pygame.K_r:
                    trails.fill((0, 0, 0))
                    trail = not trail

            if event.type == pygame.MOUSEBUTTONUP:
                if trails_button.rect.collidepoint(pygame.mouse.get_pos()):
                    print("Clicked")
                    trail = not trail
                    print(trail)
                if not trails_button.collision():
                    if temp_obj_pos:
                        objects.append(create_ship(temp_obj_pos, mouse_pos))
                        temp_obj_pos = None
                    else:
                        temp_obj_pos = mouse_pos
                else:
                    pass

        win.blit(BG, (0, 0))
        if trail:
            win.blit(trails, (0, 0))
        else:
            trails.fill((0, 0, 0))


        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > WIDTH
            collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()
        trails_button.update(win)
        pygame.display.update()

    pygame.quit()


if __name__ == "__simulator__":
    main()
