import pygame
import time
import random
from player import PlayerShip, Bullet
from enemy import Enemy

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FRAME_WIDTH, FRAME_HEIGHT = 64, 64
FPS = 2  # 2 frames per second
BG_SWITCH_INTERVAL_SEC = 120  # switch every 2 minutes

# === Background Handler ===
class BackgroundAnimator:
    def __init__(self, sprite_paths):
        self.frames = [self.load_frames_from_sheet(path) for path in sprite_paths]
        self.current_bg_index = 0
        self.current_frame_index = 0
        self.last_frame_time = time.time()
        self.last_bg_switch_time = time.time()

    def load_frames_from_sheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(4):
            frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
            frame = pygame.transform.scale(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
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
            self.current_bg_index = (self.current_bg_index + 1) % len(self.frames)
            self.current_frame_index = 0
            self.last_bg_switch_time = now

    def draw(self, surface):
        surface.blit(self.frames[self.current_bg_index][self.current_frame_index], (0, 0))


# === Main Game Setup ===
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Platypus Out of Clay")
    clock = pygame.time.Clock()

    # Load background animator
    sprite_sheet_files = [f"GIF_2FPS/space{i}_4-frames.png" for i in range(1, 10)]
    background = BackgroundAnimator(sprite_sheet_files)

    # Create player (spawned near left side, vertically centered)
    player = PlayerShip((WINDOW_WIDTH // 12, WINDOW_HEIGHT // 2))

    # Game object tracking
    bullets = []
    enemies = []

    # Timing
    last_shot_time = 0
    fire_delay = 0.3  # seconds between bullets
    last_enemy_spawn = time.time()
    enemy_spawn_delay = 2  # seconds between enemy spawns

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

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

        # Check firing state
        player.firing = keys[pygame.K_SPACE]

        # Auto-fire bullets if spacebar is held
        if player.firing:
            now = time.time()
            if now - last_shot_time > fire_delay:
                bullet_start_pos = (
                    player.rect.centerx + player.rect.width // 2, player.rect.centery)
                bullets.append(Bullet(player.auto_cannon_bullet_path, bullet_start_pos))
                last_shot_time = now

        # Spawn enemies
        now = time.time()
        if now - last_enemy_spawn > enemy_spawn_delay:
            enemies.append(Enemy())
            last_enemy_spawn = now

        # === Update + Draw ===
        background.update()
        background.draw(screen)
        player.draw(screen)

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.rect.left > WINDOW_WIDTH:
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)
            if enemy.is_off_screen():
                enemies.remove(enemy)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
