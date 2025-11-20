# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import Entity, AnimatedEntity


class Gem(Entity):

    def __init__(self, game, location, image):
        super().__init__(game, location, image)

    def apply(self, character):
        self.game.score += settings.GEM_VALUE


class Heart(Entity):

    def __init__(self, game, location, image):
        super().__init__(game, location, image)

    def apply(self, character):
        if character.hearts < character.max_hearts:
            character.hearts += 1
        

class Key(Entity):

    def __init__(self, game, location, image, code=None):
        super().__init__(game, location, image)
        
        self.code = code

    def apply(self, character):
        character.key_chain.append(self.code)
