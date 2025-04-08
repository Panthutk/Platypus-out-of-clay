# === enemy.py ===
import pygame
import random
import time

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# === Enemy Ship Types ===
ENEMY_TYPES = [
    {
        "name": "Fighter",
        "path": "Enemy/EnemyShipAsset/Base/Fighter.png",
        "engine": "Enemy/EnemyShipAsset/Engines/Fighter.png",
        "weaponAnimation": "Enemy/EnemyShipAsset/Weapons/Fighter.png",
        "projectile": "Enemy/EnemyShipAsset/Projectiles/Ray.png",
        "destroyed": "Enemy/EnemyShipAsset/Destroyed/Fighter.png",
        "speed": 3,
        "size": (192, 192),
        "health": 20,
        "projectile_speed": 5,
        "score": 100,
    },
    {
        "name": "Torpedo",
        "path": "Enemy/EnemyShipAsset/Base/Torpedo.png",
        "engine": "Enemy/EnemyShipAsset/Engines/Torpedo.png",
        "weaponAnimation": "Enemy/EnemyShipAsset/Weapons/Torpedo.png",
        "projectile": "Enemy/EnemyShipAsset/Projectiles/Torpedo.png",
        "destroyed": "Enemy/EnemyShipAsset/Destroyed/Torpedo.png",
        "speed": 2.5,
        "size": (192, 192),
        "health": 30,
        "projectile_speed": 4,
        "score": 150,
    },
    {
        "name": "Battlecruiser",
        "path": "Enemy/EnemyShipAsset/Base/Battlecruiser.png",
        "engine": "Enemy/EnemyShipAsset/Engines/Battlecruiser.png",
        "weaponAnimation": "Enemy/EnemyShipAsset/Weapons/Battlecruiser.png",
        "projectile": "Enemy/EnemyShipAsset/Projectiles/Rocket.png",
        "destroyed": "Enemy/EnemyShipAsset/Destroyed/Battlecruiser.png",
        "speed": 1.8,
        "size": (240, 240),
        "health": 50,
        "projectile_speed": 3,
        "score": 200,
    },
]

# Higher number = higher spawn chance
SPAWN_WEIGHTS = [10, 4, 3]  # Fighter common, Torpedo , Battlecruiser

# === Enemy Class ===


class Enemy:
    def __init__(self):
        # Choose enemy type
        data = random.choices(ENEMY_TYPES, weights=SPAWN_WEIGHTS, k=1)[0]
        self.data = data
        self.speed = data["speed"]
        self.size = data["size"]
        self.health = data["health"]
        self.score = data["score"]

        # Load and transform image
        original = pygame.image.load(data["path"]).convert_alpha()
        scaled = pygame.transform.scale(original, self.size)
        self.image = pygame.transform.rotate(scaled, 90)
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + random.randint(0, 300)
        self.rect.y = random.randint(50, WINDOW_HEIGHT - self.size[1])

        self.mask = pygame.mask.from_surface(
            self.image)  # For pixel-perfect collision

        # Destroyed animation setup
        self.destroyed = False
        self.destroyed_frames = self.load_destroyed_frames(
            data["destroyed"], frame_count=self.get_destroyed_frame_count())
        self.current_destroyed_frame = 0
        self.destroyed_fps = 30
        self.last_destroyed_update = 0
        self.destruction_finished = False

    def get_destroyed_frame_count(self):
        # Return correct frame count for each ship type
        name = self.data["name"]
        if name == "Fighter":
            return 18
        if name == "Torpedo":
            return 16
        if name == "Battlecruiser":
            return 18
        return 16

    def load_destroyed_frames(self, sheet_path, frame_count):
        # Slice explosion frames from sprite sheet
        sheet = pygame.image.load(sheet_path).convert_alpha()
        sheet_width = sheet.get_width()
        frame_width = sheet_width // frame_count
        frame_height = sheet.get_height()
        frames = []
        for i in range(frame_count):
            frame = pygame.Surface(
                (frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width,
                       0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.size)
            frame = pygame.transform.rotate(frame, 90)
            frames.append(frame)
        return frames

    def update(self):
        # Move left if not destroyed
        if not self.destroyed:
            self.rect.x -= self.speed
        # Explosion animation if destroyed
        elif not self.destruction_finished:
            now = time.time()
            if now - self.last_destroyed_update > 1 / self.destroyed_fps:
                self.current_destroyed_frame += 1
                if self.current_destroyed_frame >= len(self.destroyed_frames):
                    self.destruction_finished = True
                    self.health = 0
                self.last_destroyed_update = now

    def take_damage(self, damage):
        if not self.destroyed:
            self.health -= damage
            if self.health <= 0:
                self.trigger_destruction()

    def trigger_destruction(self):
        # Trigger the explosion animation
        self.destroyed = True
        self.current_destroyed_frame = -1  # Prevent flicker of first real frame
        # Force immediate frame 0 next update
        self.last_destroyed_update = time.time() - (1 / self.destroyed_fps)

    def draw(self, surface):
        if self.destroyed and not self.destruction_finished:
            surface.blit(
                self.destroyed_frames[self.current_destroyed_frame], self.rect)
        else:
            surface.blit(self.image, self.rect)

    def is_off_screen(self):
        # Mark for removal if offscreen or fully destroyed
        return self.rect.right < 0 or (self.destroyed and self.destruction_finished and self.health <= 0)
