import pygame
import sys
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (100, 100, 100)

# Constants
GRAVITY = 0.5
PLATFORMS = [(100, 500, 200, 20), (400, 400, 200, 20)]

# Clock
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.last_platform = None

    def update(self):
        # Apply gravity
        self.speed_y += GRAVITY
        # Move left/right
        self.rect.x += self.speed_x
        # Check collision with platforms horizontally
        self.check_collision(self.speed_x, 0)
        # Move up/down
        self.rect.y += self.speed_y
        # Check collision with platforms vertically
        self.check_collision(0, self.speed_y)

    def check_collision(self, dx, dy):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right
                elif dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.speed_y = 0
                    self.last_platform = platform
                elif dy < 0:
                    self.rect.top = platform.rect.bottom

        # If the player falls off a platform, land on the last platform
        if self.rect.top > HEIGHT:
            if self.last_platform:
                self.rect.bottom = self.last_platform.rect.top
                self.speed_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

player = Player()
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

all_sprites.add(player)

# Create platforms
for platform_data in PLATFORMS:
    platform = Platform(*platform_data)
    platforms.add(platform)
    all_sprites.add(platform)

# Load background image
background_path = "background.png"
if not os.path.exists(background_path):
    print(f"Error: Background image '{background_path}' not found.")
    sys.exit()

background = pygame.image.load(background_path).convert()
background_rect = background.get_rect()
background_scroll = 0

def game_loop():
    global background_scroll

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # Move left/right
        if keys[pygame.K_LEFT]:
            player.speed_x = -5
            if background_scroll < 0:
                background_scroll += 5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
            if background_scroll > WIDTH - background_rect.width:
                background_scroll -= 5
        else:
            player.speed_x = 0

        all_sprites.update()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background, (background_scroll, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

game_loop()
