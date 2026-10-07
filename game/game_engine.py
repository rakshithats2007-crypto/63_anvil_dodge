import pygame
import random

from game.player import Player
from game.anvil import Anvil


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(width, height)
        self.anvils = []

        # Task 4: impact effects
        self.particles = []
        self.screen_shake = 0

        self.spawn_delay = 700
        self.last_spawn_time = pygame.time.get_ticks()

        self.start_ticks = pygame.time.get_ticks()
        self.survival_time = 0
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 52)
        self.font_medium = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

        self.player.update()

        # Calculate survival time
        self.survival_time = (
            pygame.time.get_ticks() - self.start_ticks
        ) // 1000

        # ---------------------------------
        # Task 2: Dynamic Difficulty Scaling
        # ---------------------------------

        now = pygame.time.get_ticks()

        # Difficulty increases gradually over 30 seconds
        difficulty_level = min(self.survival_time / 30.0, 1.0)

        # Anvil speed increases by maximum 40%
        speed_multiplier = 1.0 + (0.4 * difficulty_level)

        # Spawn delay decreases from 700 ms to minimum 450 ms
        current_spawn_delay = max(
            450,
            int(700 - (250 * difficulty_level))
        )

        if now - self.last_spawn_time >= current_spawn_delay:
            self.anvils.append(
                Anvil(self.width, speed_multiplier)
            )
            self.last_spawn_time = now

        # ---------------------------------
        # Update anvils
        # ---------------------------------

        player_rect = self.player.rect

        for anvil in self.anvils[:]:
            anvil.update()

            # Collision remains unchanged
            if player_rect.colliderect(anvil.rect):
                self.game_state = "GAME_OVER"

            # Anvil reaches the ground
            if anvil.is_off_screen(self.height):
                self.create_impact_effect(
                    anvil.x + anvil.width // 2,
                    self.height - 20
                )

                self.anvils.remove(anvil)

        # ---------------------------------
        # Task 4: Update impact particles
        # ---------------------------------

        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # Gravity
            particle["vy"] += 0.2

            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

        # Gradually stop screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def create_impact_effect(self, x, y):
        # Create small particles
        for _ in range(12):
            particle = {
                "x": x,
                "y": y,
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-4, -1),
                "life": 20
            }

            self.particles.append(particle)

        # Start screen shake
        self.screen_shake = 6

    def reset(self):
        self.player = Player(self.width, self.height)
        self.anvils.clear()

        # Clear Task 4 effects
        self.particles.clear()
        self.screen_shake = 0

        self.start_ticks = pygame.time.get_ticks()
        self.last_spawn_time = pygame.time.get_ticks()

        self.survival_time = 0
        self.game_state = "PLAYING"

    def render(self, screen):
        # Create temporary surface for the game
        game_surface = pygame.Surface(
            (self.width, self.height)
        )

        game_surface.fill((35, 38, 45))

        ground_y = self.height - 20

        pygame.draw.rect(
            game_surface,
            (70, 75, 85),
            (0, ground_y, self.width, 20)
        )

        pygame.draw.line(
            game_surface,
            (160, 90, 40),
            (0, ground_y),
            (self.width, ground_y),
            3
        )

        # Draw player
        self.player.render(game_surface)

        # Draw anvils
        for anvil in self.anvils:
            anvil.render(game_surface)

        # ---------------------------------
        # Task 4: Draw impact particles
        # ---------------------------------

        for particle in self.particles:
            pygame.draw.circle(
                game_surface,
                (230, 180, 80),
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                3
            )

        # Survival time
        time_surf = self.font_medium.render(
            f"Survival Time: {self.survival_time}s",
            True,
            (240, 240, 240)
        )

        game_surface.blit(
            time_surf,
            (20, 20)
        )

        # Instructions
        inst_surf = self.font_small.render(
            "Use [A/D] or [Arrow Keys] to Dodge",
            True,
            (170, 175, 185)
        )

        game_surface.blit(
            inst_surf,
            (
                self.width - inst_surf.get_width() - 20,
                25
            )
        )

        # ---------------------------------
        # Game Over screen
        # ---------------------------------

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 190))

            game_surface.blit(
                overlay,
                (0, 0)
            )

            over_surf = self.font_big.render(
                "CRUSHED! GAME OVER",
                True,
                (235, 65, 65)
            )

            game_surface.blit(
                over_surf,
                (
                    self.width // 2
                    - over_surf.get_width() // 2,
                    self.height // 2 - 60
                )
            )

            score_surf = self.font_medium.render(
                f"You survived: {self.survival_time} seconds",
                True,
                (255, 255, 255)
            )

            game_surface.blit(
                score_surf,
                (
                    self.width // 2
                    - score_surf.get_width() // 2,
                    self.height // 2
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            game_surface.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )

        # ---------------------------------
        # Task 4: Screen shake
        # ---------------------------------

        offset_x = 0
        offset_y = 0

        if self.screen_shake > 0:
            offset_x = random.randint(
                -self.screen_shake,
                self.screen_shake
            )

            offset_y = random.randint(
                -self.screen_shake,
                self.screen_shake
            )

        # Draw final game surface
        screen.fill((35, 38, 45))

        screen.blit(
            game_surface,
            (offset_x, offset_y)
        )