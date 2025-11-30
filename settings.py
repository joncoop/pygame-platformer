# Third-party imports
import pygame


# Window settings
GRID_SIZE = 64
SCREEN_WIDTH = 16 * GRID_SIZE
SCREEN_HEIGHT = 9 * GRID_SIZE
CAPTION = "My Awesome Game"
FPS = 60
CAMERA_LAG = 0.8

# Define colors
SKY_BLUE = (135, 200, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
PRIMARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'
SECONDARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'

# Images
''' hero '''
HERO_IMGS_IDLE = ['assets/images/characters/player_idle.png']
HERO_IMGS_WALK = ['assets/images/characters/player_walk1.png',
                  'assets/images/characters/player_walk2.png']
HERO_IMGS_JUMP = ['assets/images/characters/player_jump.png']

''' tiles '''
GRASS_IMG = 'assets/images/tiles/grass_dirt.png'
BLOCK_IMG = 'assets/images/tiles/block.png'
DOOR_IMG = 'assets/images/tiles/door.png'
LOCKED_DOOR_IMG = 'assets/images/tiles/locked_door.png'
SIGN_IMG = 'assets/images/tiles/sign.png'
FLAG_IMG = 'assets/images/tiles/flag.png'
FLAGPOLE_IMG = 'assets/images/tiles/flagpole.png'

''' items '''
GEM_IMG = 'assets/images/items/gem.png'
HEART_IMG = 'assets/images/items/heart.png'
KEY_IMG = 'assets/images/items/key.png'

''' enemies '''
CLOUD_IMGS = ['assets/images/characters/cloud.png']
SPIKEBALL_IMGS = ['assets/images/characters/spikeball1.png',
                  'assets/images/characters/spikeball2.png']                   
SPIKEMAN_IMGS = ['assets/images/characters/spikeman_walk1.png',
                 'assets/images/characters/spikeman_walk2.png']

# Sounds
JUMP_SND = 'assets/sounds/jump.wav'
GEM_SND = 'assets/sounds/collect_point.wav'

# Music
TITLE_MUSIC = 'assets/music/calm_happy.ogg'
MAIN_THEME = 'assets/music/cooking_mania.wav'

# Levels
STARTING_LEVEL = 6

LEVELS = [
    'assets/levels/world-1.json',
    'assets/levels/world-2.json',
    'assets/levels/world-3.json',
    'assets/levels/world-4.json',
    'assets/levels/world-5.json',
    'assets/levels/world-6.json',
    'assets/levels/world-7.json',
    'assets/levels/world-8.json',
    'assets/levels/world-9.json'
    'assets/levels/world-10.json'
]

LEVEL_TRANSITION_TIME = 120

# Default character attributes
DEFAULT_ANIMATION_FRAME_RATE = 0.1

HERO_HEARTS = 3
HERO_MAX_HEARTS = 5
HERO_SPEED = 5
HERO_JUMP_POWER = 22
HERO_EXCAPE_TIME = 180

SPIKEMAN_SPEED = 2
SPIKEBALL_SPEED = 2
CLOUD_SPEED = 3

# Item attributes
GEM_VALUE = 10

# Physics
GRAVITY = 1.0
TERMINAL_VELOCITY = 20

# Gameplay settings
CONTROLS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'jump': pygame.K_SPACE,
    'interact': pygame.K_e,
}
