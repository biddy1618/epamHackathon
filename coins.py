"""
Sprite Collect Coins

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade
import os

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING_ZOMBIE = 0.3
SPRITE_SCALING_COIN = 0.1
ZOMBIE_COUNT = 5
COIN_COUNT = 10
CELL_LENGTH = 80
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3


# Options
ZOMBIE_COUNT = 1
COIN_COUNT = 10
MAX_GRID = 7
FRAME_RATE = 1/2
ZOMBIE_SPEED = 1/5


SCREEN_SIZE = 800
CELL_LENGTH = round(SCREEN_SIZE/MAX_GRID)
SCREEN_TITLE = "Sprite Collect Coins Example"


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/character.png", SPRITE_SCALING_PLAYER)

class Zombie(arcade.Sprite):
    def __init__(self, speed=0.5):
        super().__init__("images/zombie.png", SPRITE_SCALING_ZOMBIE)
        self.direction = random.randint(0, 3)
        if speed > 1:
            self.speed = 1
        elif speed < 0:
            self.speed = 0
        else:
            self.speed = speed

class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__("images/coin_01.png", SPRITE_SCALING_COIN)
        self.direction = random.randint(0, 3)

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_SIZE, SCREEN_SIZE, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.zombie_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Set the timer
        self.time = 0

        # State of the game
        self.END = False
        self.WIN = False

        # State of the agents
        self.state = [[0]*MAX_GRID]*MAX_GRID


        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = Player()
        self.player_sprite.center_x = CELL_LENGTH/2
        self.player_sprite.center_y = CELL_LENGTH/2
        self.player_list.append(self.player_sprite)
        self.state[0][0] = 1

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin()

            # Position the coin
            coin.center_x = random.randint(0, MAX_GRID-1) * CELL_LENGTH + CELL_LENGTH/2
            coin.center_y = random.randint(0, MAX_GRID-1) * CELL_LENGTH + CELL_LENGTH/2

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Create the zombies
        for i in range(ZOMBIE_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            zombie = Zombie(ZOMBIE_SPEED)

            # Position the coin
            zombie.center_x = random.randint(0, MAX_GRID-1) * CELL_LENGTH + CELL_LENGTH/2
            zombie.center_y = random.randint(0, MAX_GRID-1) * CELL_LENGTH + CELL_LENGTH/2

            # Add the coin to the lists
            self.zombie_list.append(zombie)

    def draw_grid(self):
        for i in range(MAX_GRID):
            arcade.draw_line(0, i*CELL_LENGTH, SCREEN_SIZE, i*CELL_LENGTH, arcade.color.BLACK, 2)
            arcade.draw_line(i*CELL_LENGTH, 0, i*CELL_LENGTH, SCREEN_SIZE, arcade.color.BLACK, 2)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        
        # draw grid
        self.draw_grid()
        
        
        self.coin_list.draw()
        self.player_list.draw()
        self.zombie_list.draw()

        if self.END:
            finish_text = f'You lost!\n Score: time-{self.time}, coins-{self.score}.'
            arcade.draw_text(finish_text, SCREEN_SIZE/2, SCREEN_SIZE/2, arcade.color.WHITE, 20)
            return
        
        if self.WIN:
            finish_text = f'You won!\n Score: time-{self.time}, coins-{self.score}.'
            arcade.draw_text(finish_text, SCREEN_SIZE/2, SCREEN_SIZE/2, arcade.color.WHITE, 20)
            return

        # Put the text on the screen.
        output = f"Score:{self.score:>3}"
        time   = f'Time :{self.time:>3}'
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 10)
        arcade.draw_text(time, 10, 7, arcade.color.WHITE, 10)


        
    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.player_sprite.center_x = (self.player_sprite.center_x - CELL_LENGTH)%SCREEN_SIZE
        elif key == arcade.key.RIGHT:
            self.player_sprite.center_x = (self.player_sprite.center_x + CELL_LENGTH)%SCREEN_SIZE
        elif key == arcade.key.UP:
            self.player_sprite.center_y = (self.player_sprite.center_y + CELL_LENGTH)%SCREEN_SIZE
        elif key == arcade.key.DOWN:
            self.player_sprite.center_y = (self.player_sprite.center_y - CELL_LENGTH)%SCREEN_SIZE
    
    
    def update(self, delta_time):
        """ Movement and game logic """
        if self.END or self.WIN:
            return
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.player_sprite.update()
        self.zombie_list.update()

        

        # Generate a list of all coins that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding coin, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1
        
        if len(self.coin_list) == 0:
            self.WIN = True
        
        # Generate a list of all zombies that collided with the player.
        zombie_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zombie_list)

        # Loop through each colliding coin, remove it, and add to the score.
        if zombie_hit_list and not self.WIN:
            self.END = True
        

        for coin in self.coin_list:
            dir = (coin.direction + random.randint(-1, 1))%4
            if dir == UP:
                coin.center_y = (coin.center_y + CELL_LENGTH)%SCREEN_SIZE
            elif dir == DOWN:
                coin.center_y = (coin.center_y - CELL_LENGTH)%SCREEN_SIZE
            elif dir == RIGHT:
                coin.center_x = (coin.center_x + CELL_LENGTH)%SCREEN_SIZE
            elif dir == LEFT:
                coin.center_x = (coin.center_x - CELL_LENGTH)%SCREEN_SIZE
            coin.direction=dir
        
        for zombie in self.zombie_list:
            if random.random() > zombie.speed:
                dir = 4
            else:
                zombie.direction = (zombie.direction + random.randint(-1, 1))%4
                dir = zombie.direction
            if dir == UP:
                zombie.center_y = (zombie.center_y + CELL_LENGTH)%SCREEN_SIZE
            elif dir == DOWN:
                zombie.center_y = (zombie.center_y - CELL_LENGTH)%SCREEN_SIZE
            elif dir == RIGHT:
                zombie.center_x = (zombie.center_x + CELL_LENGTH)%SCREEN_SIZE
            elif dir == LEFT:
                zombie.center_x = (zombie.center_x - CELL_LENGTH)%SCREEN_SIZE

        self.time += 1

def solve(state):
    pass
        


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    window.set_update_rate(FRAME_RATE)
    arcade.run()


if __name__ == "__main__":
    main()