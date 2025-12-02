# Standard Library Imports

# Third-Party Imports
import pygame

# Local Imports
import settings
from .entity import AnimatedEntity


class Hero(AnimatedEntity):

    def __init__(self, game, location, animations, controls):
        super().__init__(game, location, animations, default_animation_key="idle_right") 

        self.controls = controls
        self.vx = 0
        self.vy = 0
        self.hearts = settings.HERO_HEARTS
        self.max_hearts = settings.HERO_MAX_HEARTS
        self.escape_time = 0
        self.facing_right = True
        self.respawn_point = location  # actually gets set in load level, location is None at instantiation (should this just be saved in game?)
        self.key_chain = []
    
    def act(self, events, pressed_keys):
        if pressed_keys[self.controls['left']]:
            self.go_left()
        elif pressed_keys[self.controls['right']]:
            self.go_right()
        else:
            self.stop()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROLS['jump']:
                    self.jump()
                elif event.key == settings.CONTROLS['interact']:
                    self.interact()
    
    def go_left(self):
        self.vx = -1 * settings.HERO_SPEED
        self.facing_right = False
    
    def go_right(self):
        self.vx = settings.HERO_SPEED
        self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self):
        if self.can_jump:
            self.vy = -1 * settings.HERO_JUMP_POWER

    def interact(self):
        hits = pygame.sprite.spritecollide(self, self.game.world.interactables, False)

        for interactable in hits:
            interactable.interact(self)

    @property
    def can_jump(self):
        return self.on_platform
    
    @property
    def is_alive(self):
        return self.hearts > 0

    @property
    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, self.game.world.goals)  # No collision resolution here, let hero overlap flag
    
    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.world.enemies, False)

        if self.escape_time == 0:
            for enemy in hits:
                self.escape_time = settings.HERO_ESCAPE_TIME
                self.hearts -= 1

                bouncex = 15  # Magic number alert! (Also isn't detecting which way the collision occured.)
                bouncey = -5
                if self.rect.centerx < enemy.rect.centerx:
                    bouncex *= -1

                self.vx = bouncex
                self.vy = bouncey
                # oof sound?
        else:
            self.escape_time -= 1
    
    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.world.items, True)
    
        for item in hits:
            item.apply(self)

    def check_world_bottom(self):
        off_bottom = super().check_world_bottom()

        if off_bottom:
            self.hearts -= 1

            if self.hearts > 0:
                self.move_to(self.respawn_point)

        return False

    def set_animation_key(self):
        if self.facing_right:
            if not self.on_platform:
                self.animation_key = "jump_right"
            elif self.vx > 0:
                self.animation_key = "walk_right"
            else:
                self.animation_key = "idle_right"
        else:
            if not self.on_platform:
                self.animation_key = "jump_left"
            elif self.vx < 0:
                self.animation_key = "walk_left"
            else:
                self.animation_key = "idle_left"

    def update(self):
        self.apply_gravity()
        self.check_items()        # Place here in case an item affects movement
        self.check_enemies()      # Must be before move for bounce to work
        self.move_x()
        self.check_platforms_x()  # Must resolve collisions in x-direction prior to moving in y-direction
        self.move_y()
        self.check_platforms_y()
        self.check_world_edges()
        self.check_world_bottom() # We don't need the return value for anything
        self.animate()
