import random
import pygame


class Anvil:
    def __init__(self, screen_width, speed_multiplier=1.0):
        self.screen_width = screen_width
        self.width = 40
        self.height = 32
        self.x = random.randint(20, screen_width - self.width - 20)
        self.y = -self.height
        self.speed = random.uniform(4.5, 7.0) * speed_multiplier

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def get_warning_color(self):
        if self.speed < 6.0:
            return (120, 120, 130)       # Grey
        elif self.speed < 8.0:
            return (230, 180, 50)        # Yellow / orange
        else:
            return (220, 60, 60)         # Red

    def render(self, surface):
        color = self.get_warning_color()

        top_rect = pygame.Rect(
            int(self.x) + 4,
            int(self.y),
            self.width - 8,
            14
        )

        pygame.draw.rect(
            surface,
            color,
            top_rect,
            border_radius=2
        )

        base_rect = pygame.Rect(
            int(self.x),
            int(self.y) + 14,
            self.width,
            18
        )

        pygame.draw.rect(
            surface,
            color,
            base_rect,
            border_radius=3
        )

        pygame.draw.rect(
            surface,
            (200, 200, 210),
            base_rect,
            width=1,
            border_radius=3
        )