# Standard Library Imports


# Third-Party Imports
import pygame

# Local Imports
import settings


class InfoBox:
    BOX_COLOR = settings.WHITE
    BORDER_COLOR = settings.BLACK
    TEXT_COLOR = settings.BLACK
    BORDER_RADIUS = 12
    BORDER_THICKNESS = 4
    MAX_WIDTH = settings.SCREEN_WIDTH * 0.5
    LINE_SPACING = 6
    PADDING = 24
    FONT_SIZE = 48

    def __init__(self, game, message, **kwargs):
        self.game = game
        self.message = message

        # Instance variables with defaults from class constants
        self.background_color = kwargs.get("background_color", self.BOX_COLOR)
        self.border_color = kwargs.get("border_color", self.BORDER_COLOR)
        self.border_radius = kwargs.get("border_radius", self.BORDER_RADIUS)
        self.border_thickness = kwargs.get("border_thickness", self.BORDER_THICKNESS)
        self.max_width = kwargs.get("max_width", self.MAX_WIDTH)
        self.line_spacing = kwargs.get("line_spacing", self.LINE_SPACING)
        self.padding = kwargs.get("padding", self.PADDING)
        self.text_color = kwargs.get("text_color", self.TEXT_COLOR)
        
        font_family = kwargs.get("font_family", settings.SECONDARY_FONT)
        font_size = kwargs.get("font_size", self.FONT_SIZE)
        self.font = pygame.font.Font(font_family, font_size)
        
        # Pre-render wrapped lines
        self.lines = self.wrap_text(message, self.font, self.max_width)

        # Compute box size from lines
        total_text_height = len(self.lines) * self.font.get_height() + (len(self.lines)-1) * self.line_spacing
        self.box_width = self.max_width
        self.box_height = total_text_height + self.padding * 2

        # Center box
        self.rect = pygame.Rect(0, 0, self.box_width, self.box_height)
        self.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current = []

        for word in words:
            test = " ".join(current + [word])
            if self.font.size(test)[0] <= max_width - self.PADDING * 2:
                current.append(word)
            else:
                lines.append(" ".join(current))
                current = [word]

        if current:
            lines.append(" ".join(current))

        return lines

    def update(self):
        pass

    def draw(self, surface):
        # Draw box
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, width=self.border_thickness, border_radius=self.border_radius)
        
        # Draw each line of text
        x = self.rect.x + self.PADDING
        y = self.rect.y + self.PADDING
        
        for line in self.lines:
            text_surf = self.font.render(line, True, self.text_color)
            surface.blit(text_surf, (x, y))
            y += text_surf.get_height() + self.line_spacing


class SignText(InfoBox):
    def __init__(self, game, message):
        super().__init__(
            game, 
            message,
            font_size=48,
            background_color=(174, 118, 64),
            border_color=(115, 97, 80),
            text_color=(255, 255, 255)
        )

    def act(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROLS['interact']:
                    self.game.infobox = None
                    self.game.current_scene = self.game.PLAYING


class SpeechBubble:

    def __init__(self, game, dialog, npc):
        super().__init__(
            game, 
            dialog
        )
        self.current_page = 0

    def act(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROLS['interact']:
                    self.game.infobox = None
                    self.game.current_scene = self.game.PLAYING
                elif event.key == settings.CONTROLS['right']:
                    self.current_page += 1