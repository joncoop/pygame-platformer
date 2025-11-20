# Standard Library Imports


# Third-Party Imports
import pygame

# Local Imports
import settings


class SignText:

    def __init__(self, game, message):
        self.game = game
        self.message = message

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render(self.message, True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)


class SpeechBubble:

    def __init__(self, game, message):
        self.game = game
        self.message = message

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render(self.message, True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
