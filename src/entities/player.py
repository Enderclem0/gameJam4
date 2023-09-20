import arcade

from src.constants import *
from src.utils import load_texture_pair


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = PLAYER_SCALING

        main_path = f"../rsc/PNG/Players/128x256/Blue/alienBlue"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_stand.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_swim1.png")

        # Load textures for walking
        self.walk_textures = []
        texture = load_texture_pair(f"{main_path}_walk1.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}_walk2.png")
        self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])

        # Track our state
        self.jumping = False
        self.should_update_walk = 0
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        # if the current frame % 3 == 0... then change the texture

        if self.should_update_walk == 6:
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.should_update_walk = 0
        else:
            self.should_update_walk += 1
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
