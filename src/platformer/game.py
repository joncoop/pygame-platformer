# Standard library
import json

# Third-party
import pygame

# Local
import platformer.camera
import platformer.entities
import platformer.overlays
import settings


# Main game class 
class Game:

    # Scenes
    START = 0
    PLAYING = 1
    INTERACTING = 2
    PAUSE = 3
    LEVEL_COMPLETE = 4
    WIN = 5
    LOSE = 6

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.make_overlays()
        self.new_game()

    def load_assets(self):
        # Platforms
        self.grass_dirt_img = pygame.image.load(settings.GRASS_IMG).convert_alpha()
        self.block_img = pygame.image.load(settings.BLOCK_IMG).convert_alpha()
        
        # Hero
        self.hero_animations = {
            "idle_right": [pygame.image.load(path).convert_alpha() for path in settings.HERO_IMGS_IDLE],
            "walk_right": [pygame.image.load(path).convert_alpha() for path in settings.HERO_IMGS_WALK],
            "jump_right": [pygame.image.load(path).convert_alpha() for path in settings.HERO_IMGS_JUMP],
        }
        self.hero_animations["idle_left"] = [pygame.transform.flip(image, True, False) for image in self.hero_animations["idle_right"]]
        self.hero_animations["walk_left"] = [pygame.transform.flip(image, True, False) for image in self.hero_animations["walk_right"]]
        self.hero_animations["jump_left"] = [pygame.transform.flip(image, True, False) for image in self.hero_animations["jump_right"]]

        # Enemies
        self.cloud_animations = {
            "default": [pygame.image.load(path).convert_alpha() for path in settings.CLOUD_IMGS]
        }

        self.spikeball_animations = {
            "default": [pygame.image.load(path).convert_alpha() for path in settings.SPIKEBALL_IMGS]
        }

        self.spikeman_animations = {
            "walk_right": [pygame.image.load(path).convert_alpha() for path in settings.SPIKEMAN_IMGS]
        }
        self.spikeman_animations["walk_left"] = [pygame.transform.flip(image, True, False) for image in self.spikeman_animations["walk_right"]]
        
        # Items
        self.gem_img = pygame.image.load(settings.GEM_IMG).convert_alpha()
        self.heart_img = pygame.image.load(settings.HEART_IMG).convert_alpha()
        self.key_img = pygame.image.load(settings.KEY_IMG).convert_alpha()

        # Interactables
        self.door_img = pygame.image.load(settings.DOOR_IMG).convert_alpha()
        self.locked_door_img = pygame.image.load(settings.LOCKED_DOOR_IMG).convert_alpha()
        self.sign_img = pygame.image.load(settings.SIGN_IMG).convert_alpha()
        self.shopkeeper_img = pygame.image.load(settings.SHOPKEEPER_IMG).convert_alpha()
        self.wizard_img = pygame.image.load(settings.WIZARD_IMG).convert_alpha()

        # Goal
        self.flag_img = pygame.image.load(settings.FLAG_IMG).convert_alpha()
        self.flagpole_img = pygame.image.load(settings.FLAGPOLE_IMG).convert_alpha()

    def make_overlays(self):
        self.scene_overlays = {
            Game.START: platformer.overlays.TitleScreen(self),
            Game.WIN: platformer.overlays.WinScreen(self),
            Game.LOSE:platformer.overlays.LoseScreen(self),
            Game.LEVEL_COMPLETE:platformer.overlays.LevelCompleteScreen(self),
            Game.PAUSE: platformer.overlays.PauseScreen(self),
        }

        self.hud = platformer.overlays.HUD(self)
        self.grid = platformer.overlays.Grid(self)
        
    def new_game(self):
        # Make the hero here so it persists across levels
        self.players = pygame.sprite.Group()
        self.hero = platformer.entities.Hero(self, None, self.hero_animations, settings.CONTROLS)
        self.players.add(self.hero)

        # Go to first level
        self.current_scene = Game.START
        self.level = settings.STARTING_LEVEL
        self.score = 0
        self.load_level()
    
    def load_level(self):
        # Make sprite groups
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()

        # Load the level data
        first_level = settings.LEVELS[self.level - 1]
        with open(first_level) as f:
            self.data = json.load(f)

        # World settings
        self.world_width = self.data['width'] * settings.GRID_SIZE
        self.world_height = self.data['height'] * settings.GRID_SIZE
        self.camera = platformer.camera.ScrollingCamera(self.screen, [self.world_width, self.world_height], self.hero, settings.CAMERA_LAG)

        # Position the hero
        location = self.data['start']
        self.hero.move_to(location)
        self.hero.respawn_point = location

        # Add the platforms
        if 'grass' in self.data:   
            for location in self.data['grass']:
                self.platforms.add( platformer.entities.Tile(self, location, self.grass_dirt_img) )

        if 'blocks' in self.data:    
            for location in self.data['blocks']:
                self.platforms.add( platformer.entities.Tile(self, location, self.block_img) )
        
        # Add the enemies
        if 'clouds' in self.data:    
            for location in self.data['clouds']:
                self.enemies.add( platformer.entities.Cloud(self, location, self.cloud_animations) )
        
        if 'spikeballs' in self.data:    
            for location in self.data['spikeballs']:
                self.enemies.add( platformer.entities.Spikeball(self, location, self.spikeball_animations) )
        
        if 'spikemen' in self.data:    
            for location in self.data['spikemen']:
                self.enemies.add( platformer.entities.Spikeman(self, location, self.spikeman_animations) )
        
        # Items
        if 'gems' in self.data:    
            for location in self.data['gems']:
                self.items.add( platformer.entities.Gem(self, location, self.gem_img) )
        
        if 'hearts' in self.data:    
            for location in self.data['hearts']:
                self.items.add( platformer.entities.Heart(self, location, self.heart_img) )
        
        if 'keys' in self.data:    
            for data in self.data['keys']:
                location = data['loc']
                code = data['code'] if 'code' in data else None                
                self.items.add( platformer.entities.Key(self, location, self.key_img, code) )
        
        # Interactables
        if 'doors' in self.data:    
            for data in self.data['doors']:
                location = data['loc']
                destination = data['dest']
                code = data['code'] if 'code' in data else None
                image = self.locked_door_img if 'code' in data else self.door_img
                self.interactables.add( platformer.entities.Door(self, location, image, destination, code) )
        
        if 'signs' in self.data:    
            for data in self.data['signs']:
                location = data['loc']
                message = data['message']
                self.interactables.add( platformer.entities.Sign(self, location, self.sign_img, message) )

        if 'npcs' in self.data:    
            for data in self.data['npcs']:
                location = data['loc']
                message = data['message']
                if data['type'] == 'shopkeeper':
                    image = self.shopkeeper_img
                elif data['type'] == 'wizard':
                    image = self.wizard_img
                self.interactables.add( platformer.entities.NPC(self, location, image, message) )

        self.infobox = None
        
        # Goals
        if 'flag' in self.data:    
            for i, location in enumerate(self.data['flag']):
                if i == 0:
                    self.goals.add( platformer.entities.Tile(self, location, self.flag_img) )
                else:
                    self.goals.add( platformer.entities.Tile(self, location, self.flagpole_img) ) 

        # Make one big sprite group for easy updating and drawing
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.players, self.platforms, self.enemies, self.items, self.interactables, self.goals)

    def start_level(self):
        self.current_scene = Game.PLAYING

    def toggle_pause(self):
        if self.current_scene == Game.PLAYING:
            self.current_scene = Game.PAUSE
        elif self.current_scene == Game.PAUSE:
            self.current_scene = Game.PLAYING

    def complete_level(self):
        self.current_scene = Game.LEVEL_COMPLETE

    def advance(self):
        self.level += 1
        self.load_level()
        self.start_level()

    def win(self):
        self.current_scene = Game.WIN

    def lose(self):
        self.current_scene = Game.LOSE

    def check_status(self):
        if self.current_scene == Game.PLAYING:
            if not self.hero.is_alive:
                self.lose()
            if self.hero.reached_goal:
                self.complete_level()
                self.transition_time = settings.LEVEL_TRANSITION_TIME

        elif self.current_scene == Game.LEVEL_COMPLETE:
            self.transition_time -= 1

            if self.transition_time == 0:
                if self.level < len(settings.LEVELS):
                    self.advance()
                else:
                    self.win()

    def process_input(self):
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # for editing
                if event.key == pygame.K_g:
                    self.grid.toggle()
                elif event.key == pygame.K_c:
                    self.camera.toggle()

                # start/restart/pause
                elif self.current_scene == Game.START:
                    if event.key == pygame.K_SPACE:
                        self.start_level()
                        continue
                elif self.current_scene in [Game.WIN, Game.LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()
                        continue
                elif self.current_scene in [Game.PLAYING, Game.PAUSE]:
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                        continue
                
            # actual gameplay
            filtered_events.append(event)

        if self.current_scene == Game.PLAYING:
            self.hero.act(filtered_events, pressed_keys)
        elif self.current_scene == Game.INTERACTING:
            self.infobox.act(filtered_events, pressed_keys)
     
    def update(self):
        if self.current_scene == Game.PLAYING:
            self.all_sprites.update()

        self.check_status()
        self.camera.update()

    def render(self):
        self.screen.fill(settings.SKY_BLUE)
        #self.all_sprites.draw(self.screen)

        offset_x, offset_y = self.camera.get_offsets()

        for group in [self.platforms, self.interactables, self.items, self.enemies, self.goals, self.players]:
            #for sprite in self.all_sprites:
            for sprite in group:
                x = sprite.rect.x - offset_x
                y = sprite.rect.y - offset_y
                self.screen.blit(sprite.image, [x, y])

        self.hud.draw(self.screen)

        if self.infobox is not None:
            self.infobox.draw(self.screen)
        elif self.current_scene != Game.PLAYING:
            self.scene_overlays[self.current_scene].draw(self.screen)

            self.grid.draw(self.screen, offset_x, offset_y)
            self.camera.draw(self.screen)
        
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            
            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
