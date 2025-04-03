## === enemy.py ===
import pygame
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

ENEMY_TYPES = [
    {
        "name": "Fighter",
        "path": "Enemy/EnemyShipAsset/Base/Fighter.png",
        "engine" : "Enemy/EnemyShipAsset/Engines/Fighter.png",
        "weaponAnimation" : "Enemy/EnemyShipAsset/Weapons/Fighter.png",
        "projectile" : "Enemy/EnemyShipAsset/Projectiles/Ray.png",
        "destroyed" : "Enemy/EnemyShipAsset/Destroyed/Fighter.png",
        "speed": 3,
        "size": (192,192),
        "health": 20,
        "projectile_speed": 5,
        "score": 100,
    },
    {
        "name": "Torpedo",
        "path": "Enemy/EnemyShipAsset/Base/Torpedo.png",
        "engine" : "Enemy/EnemyShipAsset/Engines/Torpedo.png",
        "weaponAnimation" : "Enemy/EnemyShipAsset/Weapons/Torpedo.png",
        "projectile" : "Enemy/EnemyShipAsset/Projectiles/Torpedo.png",
        "destroyed" : "Enemy/EnemyShipAsset/Destroyed/Torpedo.png",
        "speed": 2.5,
        "size": (192,192),
        "health": 30,
        "projectile_speed": 4,
        "score": 150,
    },
    {
        "name": "Battlecruiser",
        "path": "Enemy/EnemyShipAsset/Base/Battlecruiser.png",
        "engine" : "Enemy/EnemyShipAsset/Engines/Battlecruiser.png",
        "weaponAnimation" : "Enemy/EnemyShipAsset/Weapons/Battlecruiser.png",
        "projectile" : "Enemy/EnemyShipAsset/Projectiles/Rocket.png",
        "destroyed" : "Enemy/EnemyShipAsset/Destroyed/Battlecruiser.png",
        "speed": 1.8,
        "size": (240,240),
        "health": 50,
        "projectile_speed": 3,
        "score": 200,
    },
]
BOSSES = [
    {
        "name": "Dreadnought",
        "path": "Enemy/EnemyShipAsset/Base/Dreadnought.png",
        "engine" : "Enemy/EnemyShipAsset/Engines/Dreadnought.png",
        "weaponAnimation" : "Enemy/EnemyShipAsset/Weapons/Dreadnought.png",
        "projectile" : "Enemy/EnemyShipAsset/Projectiles/Ray.png",
        "destroyed" : "Enemy/EnemyShipAsset/Destroyed/Dreadnought.png",
        "speed": 1.0,
        "size": (400,400),
        "health": 200,
        "projectile_speed": 2,
        "score": 1000,
    },
]

# Higher number = higher spawn chance
SPAWN_WEIGHTS = [10, 4, 3]  # Fighter common, Torpedo , Battlecruiser


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
