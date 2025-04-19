# Importing
import pygame

pygame.init()

# Vars
active = True
clock = pygame.time.Clock()
FRAMES = 60
SPEED = 10

# Controls Mapping
plr_1_keys = {
    pygame.K_w: "up",
    pygame.K_s: "down",
    pygame.K_a: "left",
    pygame.K_d: "right"
}

plr_2_keys = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, img_path: str, pos: tuple):
        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, key):
        if key == "up" and self.rect.top > main_win.get_rect().top:
            self.rect.y -= SPEED
        elif key == "down" and self.rect.bottom < main_win.get_rect().bottom:
            self.rect.y += SPEED
        elif key == "left" and self.rect.left > main_win.get_rect().left:
            self.rect.x -= SPEED
        elif key == "right" and self.rect.right < main_win.get_rect().right:
            self.rect.x += SPEED

# Objects
main_win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("CatChaser 🐈‍⬛")

bg_img = pygame.transform.scale(pygame.image.load("jinxcat.jpg"), (700, 500))
plr_1 = Player("3_jinxcat.jpg", (100, 100)); plr_2 = Player("5_jinxcat.jpg", (100, 100))
players = pygame.sprite.Group()
players.add(plr_1); players.add(plr_2)

# Rendering
while active:
    main_win.blit(bg_img, (0, 0))
    players.draw(main_win)

    for evt in pygame.event.get(): # Quit
        if evt.type == pygame.QUIT:
            active = False
    
    keys = pygame.key.get_pressed()

    for key, action in plr_1_keys.items(): # Player 1
        if keys[key]:
            plr_1.update(action)
    
    for key, action in plr_2_keys.items(): # Player 2
        if keys[key]:
            plr_2.update(action)

    clock.tick(FRAMES)
    pygame.display.update()

pygame.quit()
