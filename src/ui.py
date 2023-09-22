import arcade
import os
import math

from entities.player import PlayerCharacter
from constants import *


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer for the game
        """
        super().__init__()

        # Set the path to start with this program
        self.background = arcade.SpriteList()
        self.music = None
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.e_pressed = False
        self.a_pressed = False
        self.bomb_pressed = False
        self.bomb_timer = 0

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.restart_x = None
        self.restart_y = None

        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Key to press
        self.action = ""

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.water_sound = arcade.load_sound("../rsc/water.mp3")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.checkpoint_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        self.level_sound = arcade.load_sound(":resources:music/funkyrobot.mp3", streaming=True)
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.level_sound = arcade.load_sound(":resources:music/funkyrobot.mp3")

        # Load textures for HUD
        self.red_key = arcade.load_texture("../rsc/PNG/Items/keyRed.png")
        self.green_key = arcade.load_texture("../rsc/PNG/Items/keyGreen.png")
        self.yellow_key = arcade.load_texture("../rsc/PNG/Items/keyYellow.png")
        self.blue_key = arcade.load_texture("../rsc/PNG/Items/keyBlue.png")
        self.bomb = arcade.Sprite("../rsc/PNG/Tiles/bomb.png", scale=0.5)

        self.name_to_texture = {"red": self.red_key,
                                "green": self.green_key,
                                "blue": self.blue_key,
                                "yellow": self.yellow_key,
                                "bomb": self.bomb.texture}

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        images = ("../rsc/PNG/Backgrounds/blue_land.png",
                  "../rsc/PNG/Backgrounds/colored_grass.png")
        rise = BACKGROUND_RISE_AMOUNT * SPRITE_SCALING
        for count, image in enumerate(images):
            bottom = rise * len(images)
            sprite = arcade.Sprite(image, scale=SPRITE_SCALING)
            sprite.bottom = bottom
            sprite.left = 0
            self.background.append(sprite)

            sprite = arcade.Sprite(image, scale=SPRITE_SCALING)
            sprite.bottom = bottom
            sprite.left = sprite.width
            self.background.append(sprite)

        # Map name
        map_name = "../rsc/test50.json"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_WATER: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_ENEMIES: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_FLAG: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_KEY: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DOOR: {
                "use_spatial_hash": True,
            }
        }

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Keep track of the score
        self.score = 0

        # Key to press
        self.action = ""


        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()

        if self.restart_x is None:
            self.restart_x = self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        if self.restart_y is None:
            self.restart_y = self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y

        self.player_sprite.center_x = self.restart_x
        self.player_sprite.center_y = self.restart_y

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # --- Other stuff
        # Set the background color to #d0f4f7
        arcade.set_background_color(arcade.color_from_hex_string("#d0f4f7"))

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            walls=[self.scene[LAYER_NAME_PLATFORMS], self.scene[LAYER_NAME_DOOR], self.scene[LAYER_NAME_BOMB_WALLS]],
        )
        self.music = arcade.play_sound(self.level_sound)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw background
        self.background.draw()

        # Draw our Scene
        self.scene.draw()

        # Draw the bomb
        if self.bomb_pressed:
            self.bomb.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()


        # Draw our score on the screen, scrolling it with the viewport
        coin_image = arcade.load_texture('../rsc/PNG/Items/coinGold.png')
        arcade.draw_texture_rectangle(30, 40, coin_image.width / 2, coin_image.height / 2, coin_image, 0)

        arcade.draw_text(
            self.score,
            55,
            30,
            arcade.csscolor.BLACK,
            18,
        )

        arcade.draw_text(self.action,
            SCREEN_WIDTH / 2 - 150,
            SCREEN_HEIGHT - 100,
            arcade.color.RED,
            18
        )

        # Draw HUD
        if len(self.player_sprite.inventory) == 1:
            image = self.name_to_texture[self.player_sprite.inventory[0].properties["color"]]
            arcade.draw_texture_rectangle(image.width // 2, image.height, image.width, image.height, image, 0)

    def grab_object(self):

        self.player_sprite.inventory = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_KEY],
                self.scene[LAYER_NAME_BOMB]
            ],
        )
        for collision in self.player_sprite.inventory:

            if self.scene[LAYER_NAME_KEY] in collision.sprite_lists:
                arcade.play_sound(self.checkpoint_sound)
                collision.remove_from_sprite_lists()

    def check_to_open(self):

        door_list = self.scene[LAYER_NAME_DOOR]

        for door in door_list:
            norm_vect = math.sqrt(
                (self.player_sprite.center_x - door.center_x) ** 2 + (self.player_sprite.center_y - door.center_y) ** 2)
            # If the player is close to the door and the key can open this door
            if norm_vect < 100 and door.properties["color"] == self.player_sprite.inventory[0].properties[
                "opening_color"]:
                self.player_sprite.inventory = []
                door.remove_from_sprite_lists()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if (
                    self.physics_engine.can_jump(y_distance=10)
                    and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

        if self.e_pressed:
            # if the player has an item
            if len(self.player_sprite.inventory) == 1:

                # if player has a key, check to open a door
                if "opening_color" in self.player_sprite.inventory[0].properties.keys():
                    self.check_to_open()

                else:
                    # player has a bomb
                    self.bomb.center_x = self.player_sprite.center_x + 100 * (
                        -1 if self.player_sprite.facing_direction == 1 else 1)
                    self.bomb.center_y = self.player_sprite.center_y - 20
                    self.bomb_pressed = True
                    self.bomb_timer = 120

            else:
                # else check to grab object near the player
                self.grab_object()

        if self.a_pressed and len(self.player_sprite.inventory) != 0:
            # drop the item
            self.player_sprite.inventory = []

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.Q:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.E:
            self.e_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.Q:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.E:
            self.e_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False

        self.process_keychange()

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y + 100 - (self.camera.viewport_height / 2))
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered, speed)

    def explode(self, bomb: arcade.Sprite):
        def distance(s1: arcade.Sprite, s2: arcade.Sprite):
            return math.sqrt((s1.center_x - s2.center_x) ** 2 + (s1.center_y - s2.center_y) ** 2)

        bomb_walls = self.scene[LAYER_NAME_BOMB_WALLS]
        # distance between bomb and walls
        for w in bomb_walls:
            if distance(w, bomb) < 200:
                w.remove_from_sprite_lists()
        # distance between bomb and player
        if distance(self.player_sprite, bomb) < 200:
            # apply force to player depending on the angle between the bomb and the player
            angle = math.atan2(self.player_sprite.center_y - bomb.center_y, self.player_sprite.center_x - bomb.center_x)
            self.player_sprite.change_x = math.cos(angle) * 140
            self.player_sprite.change_y = math.sin(angle) * 10

        self.bomb_pressed = False
        self.bomb_timer = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        if self.bomb_pressed:
            self.bomb_timer -= 1
            if self.bomb_timer == 0:
                self.explode(self.bomb)
        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES,
            ],
        )

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES]
        )

        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_ENEMIES],
                self.scene[LAYER_NAME_WATER],
                self.scene[LAYER_NAME_FLAG],
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_EXIT]
                self.scene[LAYER_NAME_KEY],
                self.scene[LAYER_NAME_BOMB]
            ],
        )

        grab = False

        for collision in player_collision_list:
            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.stop_sound(self.music)
                arcade.play_sound(self.game_over)
                game_over = GameOverView(self, "normal")
                self.window.show_view(game_over)
                return
            elif self.scene[LAYER_NAME_WATER] in collision.sprite_lists:
                arcade.stop_sound(self.music)
                arcade.play_sound(self.water_sound)
                game_over = GameOverView(self, "water")
                self.window.show_view(game_over)
                return
            elif self.scene[LAYER_NAME_EXIT] in collision.sprite_lists:
                game_over = GameOverView(self, "win")
                self.window.show_view(game_over)
                return
            elif self.scene[LAYER_NAME_FLAG] in collision.sprite_lists:
                self.restart_x = self.player_sprite.center_x
                self.restart_y = self.player_sprite.center_y
                arcade.play_sound(self.checkpoint_sound)
                collision.remove_from_sprite_lists()
                return
            elif self.scene[LAYER_NAME_COINS] in collision.sprite_lists:
                arcade.play_sound(self.collect_coin_sound)
                points = 1
                self.score += points
                collision.remove_from_sprite_lists()
                return
                
            
            elif self.scene[LAYER_NAME_KEY] in collision.sprite_lists or self.scene[LAYER_NAME_BOMB] in collision.sprite_lists:
                grab = True


        # Update action text        
        _, distance_door = arcade.get_closest_sprite(self.player_sprite, self.scene[LAYER_NAME_DOOR])


        if distance_door < 100 and len(self.player_sprite.inventory) > 0:
            self.action = 'Press E to open the door'
        elif grab:
            self.action = 'Press E to grab the object'
        elif len(self.player_sprite.inventory) > 0:
            self.action = 'Press A to drop the key'
        else:
            self.action = ''


        # Position the camera
        self.center_camera_to_player()
        camera_x = self.camera.position[0]

        for count, sprite in enumerate(self.background):
            layer = count // 2
            frame = count % 2
            offset = camera_x / (2 ** (layer + 1))
            jump = (camera_x - offset) // sprite.width
            final_offset = offset + (jump + frame) * sprite.width
            sprite.left = final_offset

        if self.player_sprite.center_y < 0:
            self.player_sprite.center_y = 10000


class GameOverView(arcade.View):
    """Class to manage the game overview"""

    def __init__(self, game_view: arcade.View, mode):
        """This is run once when we switch to this view"""
        super().__init__()
        self.game_view = game_view

        self.background = arcade.load_texture(f"../rsc/PNG/Menu/Game_over_{mode}.jpg")

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background
                                            )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        if self.game_view is not None:
            self.window.show_view(self.game_view)
        else:
            self.window.show_view(GameView())
