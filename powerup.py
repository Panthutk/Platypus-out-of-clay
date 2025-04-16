import pygame

WINDOW_HEIGHT = 720

POWERUP_TYPES = {
    "SG": {
        "label": "SG",
        "color": (255, 215, 0),
        "duration": 10,
        "effect": "shotgun"
    },
    "IF": {
        "label": "IF",
        "color": (0, 255, 255),
        "duration": 8,
        "effect": "firerate"
    }
}


class PowerUp:
    def __init__(self, x, y, type):
        self.type = type
        data = POWERUP_TYPES[type]
        self.effect = data["effect"]
        self.duration = data["duration"]

        # Text-based rendering
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.text = self.font.render(data["label"], True, data["color"])
        self.rect = self.text.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.text)
        self.fall_speed = 2

    def update(self):
        self.rect.y += self.fall_speed

    def draw(self, surface):
        surface.blit(self.text, self.rect)

    def is_off_screen(self):
        return self.rect.top > WINDOW_HEIGHT
