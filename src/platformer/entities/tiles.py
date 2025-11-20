# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import Entity, AnimatedEntity


class Tile(Entity):

    def __init__(self, game, location, image):
        super().__init__(game, location, image)


class AnimatedTile(AnimatedEntity):

    def __init__(self, game, location, animations):
        super().__init__(game, location, animations, default_animation_key="default")

    def update(self):
        self.animate()


