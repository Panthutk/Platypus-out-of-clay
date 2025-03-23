import pygame
import sys
import os
import time  # standard Python time module

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FRAME_WIDTH, FRAME_HEIGHT = 64, 64
FPS = 2  # 2 frames per second
BG_SWITCH_INTERVAL_SEC = 120  # switch every 2 minutes

# Init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Animated Background")
clock = pygame.time.Clock()

# Load background sprite sheets
sprite_sheet_files = [
    f"GIF_2FPS/space{i}_4-frames.png" for i in range(1, 10)
]


def load_frames_from_sheet(path):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(4):
        frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * FRAME_WIDTH,
                   0, FRAME_WIDTH, FRAME_HEIGHT))
        frame = pygame.transform.scale(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
        frames.append(frame)
    return frames


# Preload all 9 backgrounds
background_sets = [load_frames_from_sheet(p) for p in sprite_sheet_files]

# State variables
current_bg_index = 0
current_frame_index = 0
last_frame_time = time.time()
last_bg_switch_time = time.time()

# Game loop
running = True
while running:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Frame animation (FPS control)
    if now - last_frame_time >= 1 / FPS:
        current_frame_index = (current_frame_index + 1) % 4
        last_frame_time = now

    # Background switching (every 2 minutes)
    if now - last_bg_switch_time >= BG_SWITCH_INTERVAL_SEC:
        current_bg_index = (current_bg_index + 1) % len(background_sets)
        current_frame_index = 0
        last_bg_switch_time = now

    # Draw background
    screen.blit(background_sets[current_bg_index][current_frame_index], (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
