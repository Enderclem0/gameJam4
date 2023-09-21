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
        arcade.set_background_color(arcade.color.WHITE)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        # Again, method 1. Use a child class to handle events.
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)

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
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

        self.manager.enable()


    def on_hide_view(self):
        self.manager.disable()


    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()