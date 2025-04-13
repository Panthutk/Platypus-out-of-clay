# === enemy.py ===
import pygame
import random
import time
import math

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
        "projectile": "Enemy/EnemyShipAsset/Projectiles/Bolt.png",
        "destroyed": "Enemy/EnemyShipAsset/Destroyed/Fighter.png",
        "speed": 3,
        "size": (192, 192),
        "health": 20,
        "projectile_speed": 5,
        "score": 100,
        "weapon_frames": 28,
        "projectile_frames": 5,
        "fire_delay": 3,
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
        "weapon_frames": 12,
        "projectile_frames": 3,
        "fire_delay": 5,
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
        "weapon_frames": 9,
        "projectile_frames": 4,
        "fire_delay": 5,
    },
]

# Higher number = higher spawn chance
SPAWN_WEIGHTS = [10, 4, 3]  # fighter, torpedo, battlecruiser

# === Enemy Class ===


class Enemy:
    def __init__(self):
        # Choose enemy type based on weighted random
        data = random.choices(ENEMY_TYPES, weights=SPAWN_WEIGHTS, k=1)[0]
        self.data = data
        self.speed = data["speed"]
        self.size = data["size"]
        self.health = data["health"]
        self.score = data["score"]
        self.projectile_speed = data["projectile_speed"]

        # Load all required assets
        self.base_image = self.load_image(data["path"])
        self.weapon_frames = self.load_frames(
            data["weaponAnimation"], data["weapon_frames"])
        self.projectile_frames = self.load_frames(
            data["projectile"], data["projectile_frames"], scale_ratio=0.25)
        self.engine_frames = self.load_frames(data["engine"], 8)
        self.destroyed_frames = self.load_frames(
            data["destroyed"], self.get_destroyed_frame_count())

        # Setup position and collision mask
        self.rect = self.base_image.get_rect()
        self.rect.x = WINDOW_WIDTH + random.randint(0, 300)
        self.rect.y = random.randint(50, WINDOW_HEIGHT - self.size[1])
        self.mask = pygame.mask.from_surface(self.base_image)

        # Engine animation state
        self.current_engine_frame = 0
        self.engine_fps = 15
        self.last_engine_update = 0

        # Weapon animation state
        self.weapon_frame_index = 0
        self.weapon_fps = 10
        self.last_weapon_update = 0
        self.is_firing = False

        # Projectile logic
        self.projectiles = []
        self.projectile_lifetime = 3  # Time before it stops tracking

        # Destroyed animation state
        self.destroyed = False
        self.destruction_finished = False
        self.current_destroyed_frame = 0
        self.destroyed_fps = 30
        self.last_destroyed_update = 0

        # Fire delay tracking
        self.last_fire_time = 0
        self.spawn_time = time.time()
        self.sine_offset = random.uniform(0, 2 * math.pi)

    def get_destroyed_frame_count(self):
        # Return number of explosion frames
        name = self.data["name"]
        if name == "Fighter":
            return 18
        if name == "Torpedo":
            return 16
        if name == "Battlecruiser":
            return 18
        return 16

    def load_image(self, path):
        # Load and rotate enemy base image
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, self.size)
        return pygame.transform.rotate(img, 90)

    def load_frames(self, path, count, scale_ratio=1.0):
        # Slice frames from sprite sheet
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // count
        frame_height = sheet.get_height()
        frames = []
        for i in range(count):
            frame = pygame.Surface(
                (frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width,
                       0, frame_width, frame_height))
            scaled_size = (
                int(self.size[0] * scale_ratio), int(self.size[1] * scale_ratio))
            frame = pygame.transform.scale(frame, scaled_size)
            frame = pygame.transform.rotate(frame, 90)
            frames.append(frame)
        return frames

    def update(self, player):
        # Update behavior every frame
        now = time.time()

        if not self.destroyed:
            # Move enemy to the left
            self.rect.x -= self.speed

            # Fighter moves randomly up/down and fires forward
            if self.data["name"] == "Fighter":
                if not self.is_firing and now - self.last_fire_time > self.data["fire_delay"]:
                    self.is_firing = True
                    self.weapon_frame_index = 0
                    self.last_weapon_update = now

                if self.is_firing:
                    if now - self.last_weapon_update > 1 / self.weapon_fps:
                        self.weapon_frame_index += 1
                        self.last_weapon_update = now

                        if self.weapon_frame_index == 4:
                            self.projectiles.append({
                                "x": self.rect.centerx,
                                "y": self.rect.centery,
                                "angle": 0,
                                "vx": -self.projectile_speed,
                                "vy": 0,
                                "start_time": now,
                                "frame": 0,
                                "frame_timer": now,
                                "state": "moving"
                            })

                        if self.weapon_frame_index >= len(self.weapon_frames):
                            self.is_firing = False
                            self.last_fire_time = now

                if not hasattr(self, 'vertical_direction'):
                    self.vertical_direction = random.choice([-1, 1])
                    self.vertical_timer = now

                if now - self.vertical_timer > random.uniform(1, 3):
                    self.vertical_direction *= -1
                    self.vertical_timer = now

                self.rect.y += self.vertical_direction * self.speed

                if self.rect.top < 0:
                    self.rect.top = 0
                    self.vertical_direction = 1
                elif self.rect.bottom > WINDOW_HEIGHT:
                    self.rect.bottom = WINDOW_HEIGHT
                    self.vertical_direction = -1

            # Torpedo moves in sine wave
            elif self.data["name"] == "Torpedo":
                t = now - self.spawn_time
                self.rect.y += math.sin(t * 4 + self.sine_offset) * 2

                # Fire downward projectile every 5 seconds
                if now - self.last_fire_time > self.data["fire_delay"]:
                    self.projectiles.append({
                        "x": self.rect.centerx,
                        "y": self.rect.bottom,
                        "angle": math.pi / 2,
                        "vx": 0,
                        "vy": self.projectile_speed,
                        "start_time": now,
                        "frame": 0,
                        "frame_timer": now,
                        "state": "moving"
                    })
                    self.last_fire_time = now

            # Battlecruiser shooting logic
            if self.data["name"] == "Battlecruiser":
                if not self.is_firing and now - self.last_fire_time > self.data["fire_delay"]:
                    self.is_firing = True
                    self.weapon_frame_index = 0
                    self.last_weapon_update = now

            # Animate engine
            if now - self.last_engine_update > 1 / self.engine_fps:
                self.current_engine_frame = (
                    self.current_engine_frame + 1) % len(self.engine_frames)
                self.last_engine_update = now

            # Weapon firing animation
            if self.is_firing:
                if now - self.last_weapon_update > 1 / self.weapon_fps:
                    self.weapon_frame_index += 1
                    self.last_weapon_update = now

                    # Fire projectile at frame 4 (Battlecruiser only)
                    if self.weapon_frame_index == 4 and self.data["name"] == "Battlecruiser":
                        dx = player.rect.centerx - self.rect.centerx
                        dy = player.rect.centery - self.rect.centery
                        angle = math.atan2(dy, dx)
                        self.projectiles.append({
                            "x": self.rect.centerx,
                            "y": self.rect.centery,
                            "angle": angle,
                            "vx": math.cos(angle) * self.projectile_speed,
                            "vy": math.sin(angle) * self.projectile_speed,
                            "start_time": now,
                            "frame": 0,
                            "frame_timer": now,
                            "state": "tracking"
                        })

                    # End of firing animation
                    if self.weapon_frame_index >= len(self.weapon_frames):
                        self.is_firing = False
                        self.last_fire_time = now

            # Update all projectiles
            for p in self.projectiles:
                if p["state"] == "tracking" and now - p["start_time"] > self.projectile_lifetime:
                    p["state"] = "moving"

                p["x"] += p["vx"]
                p["y"] += p["vy"]

                if now - p["frame_timer"] > 0.1:
                    p["frame"] = (p["frame"] + 1) % len(self.projectile_frames)
                    p["frame_timer"] = now

        elif not self.destruction_finished:
            # Update explosion animation
            if now - self.last_destroyed_update > 1 / self.destroyed_fps:
                self.current_destroyed_frame += 1
                if self.current_destroyed_frame >= len(self.destroyed_frames):
                    self.destruction_finished = True
                    self.health = 0
                self.last_destroyed_update = now

    def draw(self, surface):
        # Draw engine effect
        if not self.destroyed:
            surface.blit(
                self.engine_frames[self.current_engine_frame], self.rect)

            # Draw weapon animation if firing
            if self.is_firing:
                surface.blit(self.weapon_frames[self.weapon_frame_index % len(
                    self.weapon_frames)], self.rect)
            else:
                surface.blit(self.base_image, self.rect)
        elif not self.destruction_finished:
            # Draw explosion animation
            surface.blit(
                self.destroyed_frames[self.current_destroyed_frame], self.rect)

        # Draw all projectiles
        for p in self.projectiles:
            img = self.projectile_frames[p["frame"]]
            if p["vx"] > 0:
                img = pygame.transform.flip(img, True, False)
            rect = img.get_rect(center=(p["x"], p["y"]))
            surface.blit(img, rect)

    def take_damage(self, dmg):
        # Subtract health and trigger destruction if zero
        if not self.destroyed:
            self.health -= dmg
            if self.health <= 0:
                self.trigger_destruction()

    def trigger_destruction(self):
        # Start explosion animation
        self.destroyed = True
        self.current_destroyed_frame = -1
        self.last_destroyed_update = time.time() - (1 / self.destroyed_fps)

    def is_off_screen(self):
        # Check if enemy should be removed
        return self.rect.right < 0 or (self.destroyed and self.destruction_finished and self.health <= 0)
