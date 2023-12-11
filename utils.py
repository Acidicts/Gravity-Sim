import pygame

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mouse_pos = pygame.mouse.get_pos()
        self.down = False

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, surf):
        self.mouse_pos = pygame.mouse.get_pos()
        self.collision()
        self.draw(surf)

    def collision(self):
        if self.rect.collidepoint(self.mouse_pos):
            print("Hovering" + str(self.rect.center))
            return True


        else:
            return False
