##### MohammadAli Mirzaei #####

import arcade
from ball import Ball
from block import Block
from rocket import Rocket

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=800, title="Breakout")
        arcade.set_background_color(arcade.color.BLUE)
        self.player = Rocket(self)
        self.ball = Ball(self)
        self.block_list = arcade.SpriteList()

        for i in range(400, self.height-100, 50):
            for j in range(90, self.width-80, 80):
                new_block = Block(j, i,arcade.color.GREEN)
                new_block.center_x = j
                new_block.center_y = i
                self.block_list.append(new_block)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(250, 360, self.width-80, self.height, arcade.color.DARK_BLUE, 3)
        arcade.draw_text(f"Score: {self.player.score}", (self.width//2)+30, self.height-30, arcade.color.WHITE, 25)
        arcade.draw_text(f"HP: {self.player.health}", (self.width//2)-110, self.height-30, arcade.color.WHITE, 25)
        self.player.draw()
        self.ball.draw()
        for block in self.block_list:
            block.draw()

        if self.player.health == 0:
            arcade.draw_text("GAME OVER", (self.width//2)-95, self.height//2, arcade.color.RED, 24)
            self.player.change_x = 0
            self.player.change_y = 0
            self.ball.change_x = 0
            self.ball.change_y = 0
        arcade.finish_render()

    def on_update(self, delta_time: float):
        self.player.move()
        self.ball.move()
        
        if 50 >= self.ball.center_x or self.ball.center_x >= self.width - 50:
            self.ball.change_x *= -1

        if self.ball.center_y >= self.height - 50:
            self.ball.change_y *= -1

        if self.player.center_x <= 80:
            self.player.change_x = 0

        if self.player.center_x >= self.width -80:
            self.player.change_x = 0

        if arcade.check_for_collision(self.player, self.ball):
            self.ball.change_y *= -1

        for block in self.block_list:
            if arcade.check_for_collision(self.ball, block):
                self.player.score += 1
                self.block_list.remove(block)
                self.ball.change_y *= -1

        if self.ball.center_y < 0:
            self.player.health -= 1
            del self.ball
            self.ball = Ball(self)
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol== arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -1
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 1

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.player.width < x < self.width - self.player.width:
            self.player.change_x = 0
            self.player.center_x = x

game = Game()
arcade.run()
