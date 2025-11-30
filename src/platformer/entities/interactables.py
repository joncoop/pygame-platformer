# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import Entity, AnimatedEntity
from platformer.overlays import SignText, SpeechBubble


class Button(AnimatedEntity):

    def __init__(self, game, location, image, action):
        super().__init__(game, location, image)

        self.action = action

    def interact(self, character):
        # This is different too. A button interacts with the world, not the character.
        pass


class Door(Entity):

    def __init__(self, game, location, image, destination, code=None):
        super().__init__(game, location, image)

        self.code = code
        self.destination = destination
        self.unlocked = True if code == None else False

    def interact(self, character):
        if not self.unlocked and self.code in character.key_chain:
            self.unlocked = True
            character.key_chain.remove(self.code)
        
        if self.unlocked:
            character.move_to(self.destination)

        return None


class Sign(Entity):

    def __init__(self, game, location, image, text):
        super().__init__(game, location, image)
        self.text = text

    def interact(self, character=None):
        self.game.infobox = SignText(self.game, self.text) 
        self.game.current_scene = self.game.INTERACTING     


class NPC(Entity):

    def __init__(self, game, location, image, text):
        super().__init__(game, location, image)

        self.text = text

    def interact(self, character=None):
        self.game.infobox = SpeechBubble(self.game, self.text) 
        self.game.current_scene = self.game.INTERACTING     

    def update(self):
        pass


class Switch(AnimatedEntity):  # Similar to button but changes state rather than triggering action, maybe don't need this? button should cover it. but naming?

    def __init__(self, game, location, image, action):
        super().__init__(game, location, image)

        self.action = action

    def interact(self, character):
        pass


# This may be another type of object, interaction mechanics are different
class Crate(Entity):

    def __init__(self, game, location, image):
        super().__init__(game, location, image)

    def get_connected_crates(self, direction, connected=None):
        if connected is None:
            connected = []
        connected.append(self)

        for crate in self.game.crates:
            if direction > 0 and self.rect.right == crate.rect.left and abs(self.rect.y - crate.rect.y) <= settings.GRID_SIZE // 2:
                crate.get_connected_crates(direction, connected)
            elif direction < 0 and self.rect.left == crate.rect.right and abs(self.rect.y - crate.rect.y) <= settings.GRID_SIZE // 2:
                crate.get_connected_crates(direction, connected)

            if self.rect.top == crate.rect.bottom and abs(self.rect.x - crate.rect.x) <= settings.GRID_SIZE // 2:
                crate.get_connected_crates(direction, connected)

        return connected

    def push(self, hero):
        direction = 1 if hero.v_x > 0 else -1

        connected_crates = self.get_connected_crates(direction)

        for crate in connected_crates:
            crate.v_x = hero.v_x 
    
    def update(self):
        self.apply_gravity()
        self.move_x()
        hit_platform_x = self.check_platforms_x()
        self.move_y()
        self.check_platforms_y()
        self.check_world_edges()

        pushing = pygame.sprite.spritecollide(self, self.game.player, False)
        if not pushing:
            self.v_x = 0

        if hit_platform_x:
            self.v_x = 0
