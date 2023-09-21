
import arcade
import os

from src.entities.player import PlayerCharacter
from src.constants import *


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
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

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

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.checkpoint_sound = arcade.load_sound(":resources:sounds/hit1.wav")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Map name
        map_name = "../rsc/test10.json"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": True,
            },
        }

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()

        self.restart_x = self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        self.restart_y = self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y

        self.player_sprite.center_x = self.restart_x
        self.player_sprite.center_y = self.restart_y

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # -- Enemies
        # enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        # for my_object in enemies_layer:
        #     cartesian = self.tile_map.get_cartesian(
        #         my_object.shape[0], my_object.shape[1]
        #     )
        #     enemy_type = my_object.properties["type"]
        #     enemy = Enemy()
        #     enemy.center_x = math.floor(
        #         cartesian[0] * TILE_SCALING * self.tile_map.tile_width
        #     )
        #     enemy.center_y = math.floor(
        #         (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
        #     )
        #     if "boundary_left" in my_object.properties:
        #         enemy.boundary_left = my_object.properties["boundary_left"]
        #     if "boundary_right" in my_object.properties:
        #         enemy.boundary_right = my_object.properties["boundary_right"]
        #     if "change_x" in my_object.properties:
        #         enemy.change_x = my_object.properties["change_x"]
        #     self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

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

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        self.process_keychange()

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y - (self.camera.viewport_height / 2))
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
        """Movement and game logic"""

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
                #LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
                #LAYER_NAME_ENEMIES,
            ],
        )

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_MOVING_PLATFORMS]
        )

        # See if the enemy hit a boundary and needs to reverse direction.
        # for enemy in self.scene[LAYER_NAME_ENEMIES]:
        #     if (
        #             enemy.boundary_right
        #             and enemy.right > enemy.boundary_right
        #             and enemy.change_x > 0
        #     ):
        #         enemy.change_x *= -1
        #
        #     if (
        #             enemy.boundary_left
        #             and enemy.left < enemy.boundary_left
        #             and enemy.change_x < 0
        #     ):
        #         enemy.change_x *= -1

        # player_collision_list = arcade.check_for_collision_with_lists(
        #     self.player_sprite,
        #     [
        #         self.scene[LAYER_NAME_ENEMIES],
        #     ],
        # )

        # # Loop through each coin we hit (if any) and remove it
        # for collision in player_collision_list:
        #
        #     if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
        #         arcade.play_sound(self.game_over)
        #         game_over = GameOverView()
        #         self.window.show_view(game_over)
        #         return


        # Checkpoints
        checkpoints_collision = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_FLAG])

        if len(checkpoints_collision) > 0:

            self.restart_x = self.player_sprite.center_x
            self.restart_y = self.player_sprite.center_y

            checkpoints_collision[0].kill()

            arcade.play_sound(self.checkpoint_sound)


        # Position the camera
        self.center_camera_to_player()


class GameOverView(arcade.View):
    """Class to manage the game overview"""

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over - Click to restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameView()
        self.window.show_view(game_view)

