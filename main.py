import pygame
import sys
import os
import time  # standard Python time module

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FRAME_WIDTH, FRAME_HEIGHT = 64, 64
FPS = 2  # 2 frames per second
BG_SWITCH_INTERVAL_SEC = 120  # switch every 2 minutes


# === PlayerShip Class ===
class PlayerShip:
    def __init__(self, position):
        self.base_path = "playership/MainShip/MainShipBases"
        self.engine_base_path = "playership/MainShip/Engines/Engines.png"
        self.engine_effect_path = "playership/MainShip/Engines/Moving.png"

        self.size = 144, 144
        self.health = 4
        self.speed = 5
        self.firepower = 10

        self.position = position
        self.image = None
        self.rect = None
        self.is_moving = False

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
            self.engine_base_rect.center = center
            self.engine_effect_rect.center = center
        else:
            self.rect = self.image.get_rect(center=self.position)
            self.engine_base_rect.center = self.position
            self.engine_effect_rect.center = self.position

    def move(self, dx, dy):
        self.is_moving = dx != 0 or dy != 0

        # Calculate new position with boundaries
        new_x = max(0, min(self.rect.x + dx * self.speed,
                    WINDOW_WIDTH - self.rect.width))
        new_y = max(0, min(self.rect.y + dy * self.speed,
                    WINDOW_HEIGHT - self.rect.height))
        self.rect.x, self.rect.y = new_x, new_y

        # Update engine positions
        self.engine_base_rect.center = self.rect.center
        self.engine_effect_rect.center = self.rect.center

        # Animate effect if moving
        if self.is_moving:
            now = time.time()
            if now - self.last_engine_update > self.engine_animation_speed:
                self.current_effect_frame = (
                    self.current_effect_frame + 1) % len(self.engine_effect_frames)
                self.engine_effect_image = self.engine_effect_frames[self.current_effect_frame]
                self.last_engine_update = now

    def take_damage(self):
        if self.health > 1:
            self.health -= 1
            self.update_sprite()

    def draw(self, surface):
        # Always draw base engine first
        surface.blit(self.engine_base_image, self.engine_base_rect)

        # Draw moving effect on top if moving
        if self.is_moving:
            surface.blit(self.engine_effect_image, self.engine_effect_rect)

        # Draw ship above everything
        surface.blit(self.image, self.rect)

# === Background Handler ===


class BackgroundAnimator:
    def __init__(self, sprite_paths):
        self.frames = [self.load_frames_from_sheet(
            path) for path in sprite_paths]
        self.current_bg_index = 0
        self.current_frame_index = 0
        self.last_frame_time = time.time()
        self.last_bg_switch_time = time.time()

    def load_frames_from_sheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(4):
            frame = pygame.Surface(
                (FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * FRAME_WIDTH,
                       0, FRAME_WIDTH, FRAME_HEIGHT))
            frame = pygame.transform.scale(
                frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            frames.append(frame)
        return frames

    def update(self):
        now = time.time()
        # Frame animation
        if now - self.last_frame_time >= 1 / FPS:
            self.current_frame_index = (self.current_frame_index + 1) % 4
            self.last_frame_time = now
        # Background switching
        if now - self.last_bg_switch_time >= BG_SWITCH_INTERVAL_SEC:
            self.current_bg_index = (
                self.current_bg_index + 1) % len(self.frames)
            self.current_frame_index = 0
            self.last_bg_switch_time = now

    def draw(self, surface):
        surface.blit(self.frames[self.current_bg_index]
                     [self.current_frame_index], (0, 0))


# === Main Game Setup ===
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Platypus Out of Clay")
    clock = pygame.time.Clock()

    # Load background animator
    sprite_sheet_files = [
        f"GIF_2FPS/space{i}_4-frames.png" for i in range(1, 10)]
    background = BackgroundAnimator(sprite_sheet_files)

    # Create player (spawned near left side, vertically centered)
    player = PlayerShip((WINDOW_WIDTH // 12, WINDOW_HEIGHT // 2))

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.take_damage()  # test damage with SPACE key

        # Player movement using WASD
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a]:  # Left
            dx = -1
        if keys[pygame.K_d]:  # Right
            dx = 1
        if keys[pygame.K_w]:  # Up
            dy = -1
        if keys[pygame.K_s]:  # Down
            dy = 1
        player.move(dx, dy)

        # Update and draw everything
        background.update()
        background.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
