## === enemy.py ===
import pygame
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

ENEMY_TYPES = [
    {
        "name": "Fighter",
        "path": "Enemy/EnemyShipAsset/Base/Fighter.png",
        "speed": 3,
        "size": (144, 144),
    },
    {
        "name": "Torpedo",
        "path": "Enemy/EnemyShipAsset/Base/Torpedo.png",
        "speed": 2.5,
        "size": (144, 144),
    },
    {
        "name": "Battlecruiser",
        "path": "Enemy/EnemyShipAsset/Base/Battlecruiser.png",
        "speed": 1.8,
        "size": (192, 192),
    },
]

# Higher number = higher spawn chance
SPAWN_WEIGHTS = [10, 4, 1]  # Fighter common, Torpedo , Battlecruiser


class Enemy:
    def __init__(self):
        data = random.choices(ENEMY_TYPES, weights=SPAWN_WEIGHTS, k=1)[0]
        image_path, self.speed, size = data["path"], data["speed"], data["size"]

        original = pygame.image.load(image_path).convert_alpha()
        scaled = pygame.transform.scale(original, size)
        self.image = pygame.transform.rotate(scaled, 90)  # Face left

        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + random.randint(0, 300)
        self.rect.y = random.randint(50, WINDOW_HEIGHT - size[1])

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0
