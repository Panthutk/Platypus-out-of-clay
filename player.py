# === player.py ===
import pygame
import os
import time
import math
# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# === Bullet Class ===


class Bullet:
    def __init__(self, image_path, start_pos, speed=10):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frames = []
        self.speed_x = speed
        self.speed_y = 0
        frame_width = self.sprite_sheet.get_width() // 4
        for i in range(4):
            frame = pygame.Surface(
                (frame_width, self.sprite_sheet.get_height()), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * frame_width, 0,
                                                   frame_width, self.sprite_sheet.get_height()))
            frame = pygame.transform.rotate(frame, -90)
            self.frames.append(frame)

        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update_time = time.time()
        self.rect = self.frames[0].get_rect(center=start_pos)
        self.mask = pygame.mask.from_surface(self.frames[0])
        self.speed = speed

    def update(self):
        # Move forward
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Animate
        now = time.time()
        if now - self.last_update_time > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = now

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.rect)

# === Missile Class (FSM) ===


# === Missile Class ===
class Missile:
    def __init__(self, image_path, start_pos, player, enemies):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frames = []
        self.speed = 5
        self.state = "tracking"
        self.target = self.find_nearest_enemy(enemies, player.rect.center)
        self.start_time = time.time()
        self.lifetime = 3  # seconds

        # Resize the sprite sheet
        frame_width = self.sprite_sheet.get_width() // 3
        target_width = 64
        target_height = 64

        # load the frames
        for i in range(3):
            frame = pygame.Surface(
                (frame_width, self.sprite_sheet.get_height()), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * frame_width,
                       0, frame_width, self.sprite_sheet.get_height()))
            frame = pygame.transform.scale(
                frame, (target_width, target_height))
            frame = pygame.transform.rotate(frame, -90)
            self.frames.append(frame)

        self.current_frame = 0
        self.last_frame_time = time.time()
        self.rect = self.frames[0].get_rect(center=start_pos)
        self.mask = pygame.mask.from_surface(self.frames[0])
        self.vx, self.vy = 7, 0  # default movement

    def find_nearest_enemy(self, enemies, origin):
        if not enemies:
            return None
        return min(enemies, key=lambda e: (e.rect.centerx - origin[0]) ** 2 + (e.rect.centery - origin[1]) ** 2)

    def update(self):
        now = time.time()

        if self.state == "tracking" and self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.vx = dx / distance * self.speed
                self.vy = dy / distance * self.speed
            if now - self.start_time > self.lifetime:
                self.state = "moving"

        self.rect.x += self.vx
        self.rect.y += self.vy

        if now - self.last_frame_time > 0.1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = now

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.rect)


# === PlayerShip Class ===
class PlayerShip:
    def __init__(self, position):
        self.base_path = "playership/MainShip/MainShipBases"
        self.engine_base_path = "playership/MainShip/Engines/Engines.png"
        self.engine_effect_path = "playership/MainShip/Engines/Moving.png"
        self.auto_cannon_path = "playership/MainShip/Weapons/AutoCannon.png"
        self.auto_cannon_bullet_path = "playership/MainShipWeapon/Autocannonbullet.png"
        self.shield = "playership/MainShip/Shields/fontshield.png"

        self.size = 144, 144
        self.health = 4
        self.speed = 5
        self.firepower = 10

        self.position = position
        self.image = None
        self.rect = None
        self.is_moving = False
        self.firing = False

        # Load base engine (always visible)
        self.engine_base_image = pygame.image.load(
            self.engine_base_path).convert_alpha()
        self.engine_base_image = pygame.transform.scale(
            self.engine_base_image, self.size)
        self.engine_base_image = pygame.transform.rotate(
            self.engine_base_image, -90)
        self.engine_base_rect = self.engine_base_image.get_rect(
            center=self.position)

        # Load engine effect frames (shown when moving)
        self.engine_effect_frames = []
        effect_sheet = pygame.image.load(
            self.engine_effect_path).convert_alpha()
        frame_width = effect_sheet.get_width() // 4
        for i in range(4):
            frame = pygame.Surface(
                (frame_width, effect_sheet.get_height()), pygame.SRCALPHA)
            frame.blit(effect_sheet, (0, 0), (i * frame_width, 0,
                       frame_width, effect_sheet.get_height()))
            frame = pygame.transform.scale(frame, self.size)
            frame = pygame.transform.rotate(frame, -90)
            self.engine_effect_frames.append(frame)

        self.current_effect_frame = 0
        self.engine_animation_speed = 0.1
        self.last_engine_update = 0
        self.engine_effect_image = self.engine_effect_frames[0]
        self.engine_effect_rect = self.engine_effect_image.get_rect(
            center=self.position)

        # Load autocannon animation frames (7 total)
        self.auto_cannon_frames = []
        cannon_sheet = pygame.image.load(self.auto_cannon_path).convert_alpha()
        cannon_frame_width = cannon_sheet.get_width() // 7
        for i in range(7):
            frame = pygame.Surface(
                (cannon_frame_width, cannon_sheet.get_height()), pygame.SRCALPHA)
            frame.blit(cannon_sheet, (0, 0), (i * cannon_frame_width,
                       0, cannon_frame_width, cannon_sheet.get_height()))
            frame = pygame.transform.scale(frame, self.size)
            frame = pygame.transform.rotate(frame, -90)
            self.auto_cannon_frames.append(frame)

        self.current_cannon_frame = 0
        self.cannon_animation_speed = 0.1
        self.last_cannon_update = 0
        self.auto_cannon_image = self.auto_cannon_frames[0]
        self.auto_cannon_rect = self.auto_cannon_image.get_rect(
            center=self.position)

        # Shield attributes
        self.shield_frames = []
        self.shield_active = False
        self.shield_start_time = 0
        self.shield_duration = 3  # seconds
        self.shield_frame_index = 0
        self.shield_fps = 15
        self.last_shield_update = 0

        # Load shield animation frames (10 total)
        shield_sheet = pygame.image.load(self.shield).convert_alpha()
        shield_frame_width = shield_sheet.get_width() // 10
        for i in range(10):
            frame = pygame.Surface(
                (shield_frame_width, shield_sheet.get_height()), pygame.SRCALPHA)
            frame.blit(shield_sheet, (0, 0), (i * shield_frame_width, 0,
                       shield_frame_width, shield_sheet.get_height()))
            frame = pygame.transform.scale(frame, self.size)
            frame = pygame.transform.rotate(frame, -90)
            self.shield_frames.append(frame)

        self.update_sprite()

    def update_sprite(self):
        if self.health >= 4:
            sprite_name = "FullHealth.png"
        elif self.health == 3:
            sprite_name = "SlightDamage.png"
        elif self.health == 2:
            sprite_name = "Damaged.png"
        else:
            sprite_name = "VeryDamaged.png"

        image_path = os.path.join(self.base_path, sprite_name)
        original_image = pygame.image.load(image_path).convert_alpha()
        original_image = pygame.transform.scale(original_image, self.size)
        rotated_image = pygame.transform.rotate(original_image, -90)
        self.image = rotated_image

        if self.rect:
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect(center=self.position)

        self.engine_base_rect.center = self.rect.center
        self.engine_effect_rect.center = self.rect.center
        self.auto_cannon_rect.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)  # <- update mask here

    def move(self, dx, dy):
        self.is_moving = dx != 0 or dy != 0

        # Calculate new position with boundaries
        new_x = max(0, min(self.rect.x + dx * self.speed,
                    WINDOW_WIDTH - self.rect.width))
        new_y = max(0, min(self.rect.y + dy * self.speed,
                    WINDOW_HEIGHT - self.rect.height))
        self.rect.x, self.rect.y = new_x, new_y

        # Update engine and cannon positions
        self.engine_base_rect.center = self.rect.center
        self.engine_effect_rect.center = self.rect.center
        self.auto_cannon_rect.center = self.rect.center

        # Animate effect if moving
        if self.is_moving:
            now = time.time()
            if now - self.last_engine_update > self.engine_animation_speed:
                self.current_effect_frame = (
                    self.current_effect_frame + 1) % len(self.engine_effect_frames)
                self.engine_effect_image = self.engine_effect_frames[self.current_effect_frame]
                self.last_engine_update = now

    def take_damage(self):
        if self.shield_active:
            return  # Shield blocks the damage

        if self.health > 0:
            self.health -= 1
            self.update_sprite()
            if self.health > 0:
                self.activate_shield()

    def activate_shield(self):
        self.shield_active = True
        self.shield_start_time = time.time()
        self.shield_frame_index = 0
        self.last_shield_update = 0

    def draw(self, surface):
        # Always draw base engine first
        surface.blit(self.engine_base_image, self.engine_base_rect)

        # Animate autocannon if firing
        if self.firing:
            now = time.time()
            if now - self.last_cannon_update > self.cannon_animation_speed:
                self.current_cannon_frame = (
                    self.current_cannon_frame + 1) % len(self.auto_cannon_frames)
                self.auto_cannon_image = self.auto_cannon_frames[self.current_cannon_frame]
                self.last_cannon_update = now
        else:
            self.auto_cannon_image = self.auto_cannon_frames[0]
            self.current_cannon_frame = 0

        surface.blit(self.auto_cannon_image, self.auto_cannon_rect)

        # Draw moving effect on top if moving
        if self.is_moving:
            surface.blit(self.engine_effect_image, self.engine_effect_rect)

        # Draw shield animation if active
        if self.shield_active:
            now = time.time()
            if now - self.shield_start_time > self.shield_duration:
                self.shield_active = False
            else:
                if now - self.last_shield_update > 1 / self.shield_fps:
                    self.shield_frame_index = (
                        self.shield_frame_index + 1) % len(self.shield_frames)
                    self.last_shield_update = now
                shield_image = self.shield_frames[self.shield_frame_index]
                surface.blit(shield_image, self.rect)

        # Draw ship above everything
        surface.blit(self.image, self.rect)
