# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
PLAYER_SCALING = TILE_SCALING
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# Constants
SCREEN_TITLE = "Platformer"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 1.2
PLAYER_JUMP_SPEED = 21

LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_SPIKES = "Spike"
LAYER_NAME_KEY = "Key"
LAYER_NAME_DOOR = "Door"

# Player start position
PLAYER_START_X = 2
PLAYER_START_Y = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1