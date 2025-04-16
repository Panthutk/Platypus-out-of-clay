# === game_manager.py ===
import pygame
import time
import random
import math
from player import PlayerShip, Bullet, Missile
from enemy import Enemy
from powerup import PowerUp

pygame.font.init()
score_font = pygame.font.SysFont("Arial", 32)

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FRAME_WIDTH, FRAME_HEIGHT = 64, 64
FPS = 2  # 2 frames per second
BG_SWITCH_INTERVAL_SEC = 120  # switch every 2 minutes

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
            self.last_bg_switch_time = time.time()

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

    # Bullet tracking
    bullets = []
    enemies = []  # Enemy list
    powerups = []  # Power-up list
    missiles = []  # Missile list
    active_powerups = {}  # effect -> end_time

    last_shot_time = 0
    last_shotgun_time = 0
    fire_delay = 0.25  # 0.3 seconds between bullets
    firerate_multiplier = 1.0  # 1.0x fire rate
    shotgun_fire_delay = 0.6  # slower than regular
    enemy_spawn_delay = 2  # Spawn delay for enemies
    last_enemy_spawn = time.time()
    score = 0

    # Timer
    start_time = time.time()
    blink = False
    blink_start = 0
    blink_duration = 0.3
    last_minute_triggered = -1

    # Dificulty notification
    difficulty_msg_timer = 0
    difficulty_msg_duration = 2  # seconds
    show_difficulty_msg = False

    # Dynamic scaling factors
    enemy_health_multiplier = 1.0
    enemy_speed_multiplier = 1.0
    fire_delay_multiplier = 1.0
    enemy_projectile_speed_multiplier = 1.0  # 1.0x speed

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Player movement using WASD
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        player.move(dx, dy)

        # Check firing state
        player.firing = keys[pygame.K_SPACE]

        # Auto-fire bullets if spacebar is held
        now = time.time()
        base_x = player.rect.centerx + player.rect.width // 2
        base_y = player.rect.centery

        if player.firing:
            if "shotgun" in active_powerups and active_powerups["shotgun"] > now:
                if now - last_shotgun_time > shotgun_fire_delay:
                    # 5-way shotgun spread
                    spread_angles = [-0.4, -0.2, 0, 0.2, 0.4]
                    for angle in spread_angles:
                        vx = math.cos(angle) * 10
                        vy = math.sin(angle) * 10
                        bullet = Bullet(
                            player.auto_cannon_bullet_path, (base_x, base_y))
                        bullet.speed_x = vx
                        bullet.speed_y = vy
                        bullets.append(bullet)
                    last_shotgun_time = now
            elif "missile" in active_powerups and active_powerups["missile"] > now:
                if now - last_shot_time > 1:
                    missile = Missile(
                        "playership/MainShipWeapon/Rocket.png", (base_x, base_y), player, enemies)
                    missiles.append(missile)
                    last_shot_time = now
            else:
                if now - last_shot_time > fire_delay * fire_delay_multiplier * firerate_multiplier:

                    bullet = Bullet(
                        player.auto_cannon_bullet_path, (base_x, base_y))
                    bullets.append(bullet)
                    last_shot_time = now

        # Update and draw everything
        background.update()
        background.draw(screen)
        player.draw(screen)

        # Update bullets and check collision
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.rect.left > WINDOW_WIDTH or bullet.rect.top < 0 or bullet.rect.bottom > WINDOW_HEIGHT:
                bullets.remove(bullet)
                continue

            # Pixel-perfect bullet-enemy collision detection
            for enemy in enemies:
                offset = (enemy.rect.x - bullet.rect.x,
                          enemy.rect.y - bullet.rect.y)
                if bullet.mask.overlap(enemy.mask, offset):
                    enemy.take_damage(player.firepower)
                    if enemy.health <= 0 and enemy.destroyed:
                        if not hasattr(enemy, "powerup_dropped"):
                            enemy.powerup_dropped = True
                            score += enemy.score
                            if random.random() < 0.3:
                                selected = random.choice(["SG", "IF", "MS"])
                                powerups.append(
                                    PowerUp(enemy.rect.centerx, enemy.rect.centery, selected))
                    bullets.remove(bullet)
                    break  # Bullet hits one enemy only

        # Update missiles and check collision
        for missile in missiles[:]:
            missile.update()
            missile.draw(screen)
            if missile.rect.left > WINDOW_WIDTH or missile.rect.top < 0 or missile.rect.bottom > WINDOW_HEIGHT:
                missiles.remove(missile)
                continue
            for enemy in enemies:
                offset = (enemy.rect.x - missile.rect.x,
                          enemy.rect.y - missile.rect.y)
                if missile.mask.overlap(enemy.mask, offset):
                    enemy.take_damage(30)
                    if enemy.health <= 0 and enemy.destroyed:
                        score += enemy.score
                    if missile in missiles:
                        missiles.remove(missile)
                    break
        # Spawn new enemies
        if time.time() - last_enemy_spawn > enemy_spawn_delay:
            new_enemy = Enemy()
            new_enemy.health = int(new_enemy.health * enemy_health_multiplier)
            new_enemy.speed *= enemy_speed_multiplier
            new_enemy.projectile_speed *= enemy_projectile_speed_multiplier
            enemies.append(new_enemy)
            last_enemy_spawn = time.time()

        # Update and draw enemies
        for enemy in enemies[:]:
            enemy.update(player)
            enemy.draw(screen)

            # Pixel-perfect collision between player and enemy ship
            offset = (player.rect.x - enemy.rect.x,
                      player.rect.y - enemy.rect.y)
            if enemy.mask.overlap(player.mask, offset):
                player.take_damage()

            if enemy.is_off_screen():
                enemies.remove(enemy)

            # Pixel-perfect projectile-player collision detection
            for p in enemy.projectiles[:]:
                projectile_img = enemy.projectile_frames[p["frame"]]
                projectile_rect = projectile_img.get_rect(
                    center=(p["x"], p["y"]))
                projectile_mask = pygame.mask.from_surface(projectile_img)

                offset = (player.rect.x - projectile_rect.x,
                          player.rect.y - projectile_rect.y)
                if projectile_mask.overlap(player.mask, offset):
                    player.take_damage()
                    enemy.projectiles.remove(p)

        # === Power-up update and pickup check ===
        for pu in powerups[:]:
            pu.update()
            pu.draw(screen)
            offset = (player.rect.x - pu.rect.x, player.rect.y - pu.rect.y)
            if pu.mask.overlap(player.mask, offset):
                active_powerups[pu.effect] = time.time() + pu.duration
                powerups.remove(pu)
            elif pu.is_off_screen():
                powerups.remove(pu)

        # Score display
        score_surface = score_font.render(
            f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        # Health display
        health_surface = score_font.render(
            f"Health: {player.health}", True, (255, 255, 255))
        screen.blit(health_surface, (10, 50))

        # Timer display (top right)
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        if minutes > last_minute_triggered and minutes > 0:
            blink = True
            blink_start = time.time()
            last_minute_triggered = minutes

            # Increase difficulty every minute
            enemy_health_multiplier += 0.1  # Increase enemy health
            enemy_speed_multiplier += 0.05  # Increase enemy speed
            fire_delay_multiplier = max(
                0.1, fire_delay_multiplier - 0.02)  # Decrease fire cooldown
            # Decrease spawn delay (increase spawn rate)
            if enemy_spawn_delay > 0.3:
                enemy_spawn_delay = max(0.3, enemy_spawn_delay - 0.1)

            # Show blinking difficulty message
            show_difficulty_msg = True
            difficulty_msg_timer = time.time()

            print("Difficulty increased! New multipliers:")
            print(f"Enemy Health: {enemy_health_multiplier: .2f}, Enemy Speed: {enemy_speed_multiplier: .2f}, Fire Delay: {fire_delay_multiplier: .2f}, Spawn Delay: {enemy_spawn_delay: .2f}, Enemy Projectile Speed: {enemy_projectile_speed_multiplier: .2f}")

        if blink and time.time() - blink_start > blink_duration:
            blink = False

        if not blink:
            time_text = f"{minutes:02}:{seconds:02}"
            timer_surface = score_font.render(time_text, True, (255, 255, 255))
            screen.blit(timer_surface, (WINDOW_WIDTH -
                        timer_surface.get_width() - 10, 10))

        # Current power-ups display
        blinking = int(time.time() * 2) % 2 == 0
        current_effects = []
        has_active = False
        for key, end_time in active_powerups.items():
            remaining = end_time - time.time()
            if remaining > 0:
                has_active = True
                label = key.upper()
                if remaining <= 3 and blinking:
                    continue  # Skip rendering this tick to blink
                current_effects.append(label)
        if has_active:
            if current_effects:
                powerup_text = "Power-Ups: " + ", ".join(current_effects)
            else:
                powerup_text = "Power-Ups: "  # still show label line when blinking
        else:
            powerup_text = "Power-Ups: None"
        powerup_surface = score_font.render(
            powerup_text, True, (255, 255, 255))
        screen.blit(powerup_surface, (10, WINDOW_HEIGHT - 40))

        # Blinking "Difficulty Increased!" Message
        if show_difficulty_msg:
            if time.time() - difficulty_msg_timer < difficulty_msg_duration:
                if int(time.time() * 2) % 2 == 0:  # Blink
                    msg_surface = score_font.render(
                        "Difficulty Increased!", True, (255, 100, 100))
                    msg_rect = msg_surface.get_rect(
                        center=(WINDOW_WIDTH // 2, 30))
                    screen.blit(msg_surface, msg_rect)
            else:
                show_difficulty_msg = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
