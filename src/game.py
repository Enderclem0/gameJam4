"""
Platformer Game
"""

import arcade
import arcade.gui

from constants import *
from ui import GameView


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        # arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("rsc/PNG/Menu/Main_menu.jpg")

        start_button_style = {
            "font_name": ("time new roman", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_color": arcade.color.AMBER,
            "bg_color": (255, 191, 0)
        }


        quit_button_style = {
            "font_name": ("time new roman", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_color": arcade.color.RED,
            "bg_color": (255, 3, 62)
        }


        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, style=start_button_style)

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200, style=quit_button_style)


        # Initialise the button with an on_click event.
        @start_button.event("on_click")
        def on_click_start_button(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.show_view(game_view)


        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                align_x=165,
                align_y=125,
                child=start_button
            )
        )

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                align_x=165,
                align_y=50,
                child=quit_button
            )
        )

    def on_show_view(self):
        """Called when switching to this view."""

        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            self.background
        )

        self.manager.draw()


def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
