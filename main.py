import random

import arcade
import arcade.gui

import game_state
from attack_animation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Rock, Paper, Scissors"
DEFAULT_LINE_HEIGHT = 45

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_LEATHER_JACKET)

        self.player = arcade.Sprite("assets/guy.png")
        self.computer = arcade.Sprite("assets/computer.png", 5)
        self.players = [self.player, self.computer]
        self.rock = AttackAnimation(AttackType.ROCK)
        self.paper = AttackAnimation(AttackType.PAPER)
        self.scissors = AttackAnimation(AttackType.SCISSORS)
        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = GameState.NOT_STARTED
        self.computer_attack = random.randint(0, 2)

    def setup(self):
        pass

    def validate_victory(self):
        if self.game_state == GameState.ROUND_DONE:
            if self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.ROCK:
                self.draw_round = True
            elif self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.PAPER:
                self.player_won_round = False
                self.draw_round = False
                self.computer_score += 1
            elif self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS:
                self.player_won_round = True
                self.draw_round = False
                self.player_score += 1
            elif self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK:
                self.player_won_round = True
                self.draw_round = False
                self.player_score += 1
            elif self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.PAPER:
                self.draw_round = True
            elif self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.SCISSORS:
                self.player_won_round = False
                self.draw_round = False
                self.computer_score += 1
            elif self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.ROCK:
                self.player_won_round = False
                self.draw_round = False
                self.computer_score += 1
            elif self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER:
                self.player_won_round = True
                self.draw_round = False
                self.player_score += 1
            else:
                self.draw_round = True

    def draw_possible_attack(self):
        self.rock.center_x = 165
        self.rock.center_y = 315
        self.paper.center_x = 419
        self.paper.center_y = 325
        self.scissors.center_x = 628
        self.scissors.center_y = 324
        if self.game_state == GameState.NOT_STARTED or self.game_state == GameState.ROUND_ACTIVE:
            self.paper.draw()
            arcade.draw_rectangle_outline(405, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)
            self.rock.draw()
            arcade.draw_rectangle_outline(167, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)
            self.scissors.draw()
            arcade.draw_rectangle_outline(632, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)
        else:
            if self.player_attack_type == AttackType.ROCK:
                self.rock.draw()
                arcade.draw_rectangle_outline(167, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)
            elif self.player_attack_type == AttackType.PAPER:
                self.paper.draw()
                arcade.draw_rectangle_outline(405, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)
            else:
                self.scissors.draw()
                arcade.draw_rectangle_outline(632, 320, 170, 170, arcade.color.AIR_SUPERIORITY_BLUE, 7)

    def draw_computer_attack(self):
        arcade.draw_lrtb_rectangle_outline(1365, 1535, 405, 235, arcade.color.RADICAL_RED, 7)
        if self.game_state == GameState.ROUND_DONE or self.game_state == GameState.GAME_OVER:
            if self.computer_attack_type == AttackType.ROCK:
                self.rock_c = arcade.Sprite("assets/rockattack.png", 1.17)
                self.rock_c.center_x = 1445
                self.rock_c.center_y = 311
                self.rock_c.draw()
            elif self.computer_attack_type == AttackType.PAPER:
                self.paper_c = arcade.Sprite("assets/paper.png", 1.17)
                self.paper_c.center_x = 1460
                self.paper_c.center_y = 325
                self.paper_c.draw()
            else:
                self.scissors_c = arcade.Sprite("assets/scissors.png", 1.17)
                self.scissors_c.center_x = 1447
                self.scissors_c.center_y = 324
                self.scissors_c.draw()

    def draw_scores(self):
        player_score = f"Le pointage du joueur est {self.player_score}"
        computer_score = f"Le pointage de l'ordinateur est {self.computer_score}"
        arcade.draw_text(player_score, 195, 150, arcade.color.BLUE_SAPPHIRE, 25, width=50)
        arcade.draw_text(computer_score, 1205, 150, arcade.color.FERRARI_RED, 25, width=50)

    def draw_instructions(self):
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuyez sur 'Espace' pour commencer le round", 421, 810, arcade.color.DOLLAR_BILL, 38, width=1024)
        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text("Choisissez votre attaque à l'aide de la souris", 457, 810, arcade.color.DOLLAR_BILL, 38, width=1024)
        elif self.game_state == GameState.ROUND_DONE:
            if self.player_score < 3 and self.computer_score < 3:
                arcade.draw_text("Appuyer sur 'Espace' pour commencer un nouveau round", 491, 50, arcade.color.DOLLAR_BILL, 25, width=1024)
                if self.player_won_round == True:
                    arcade.draw_text("Le joueur a remporté le round" , 594, 810, arcade.color.DOLLAR_BILL, 40, width=1024)
                elif self.player_won_round == False and self.draw_round == False:
                    arcade.draw_text("L'ordinateur a remporté le round", 563, 810, arcade.color.DOLLAR_BILL, 40, width=1024)
                elif self.draw_round == True:
                    arcade.draw_text("Égalité", 853, 810, arcade.color.DOLLAR_BILL, 40, width=1024)

        elif self.game_state == GameState.GAME_OVER:
            if self.player_score == 3:
                arcade.draw_text("La partie est terminée, le joueur l'emporte", 478, 810, arcade.color.DOLLAR_BILL, 40, width=1024)
            if self.computer_score == 3:
                arcade.draw_text("La partie est terminée, l'ordinateur l'emporte", 464, 810, arcade.color.DOLLAR_BILL, 40, width=1024)
            arcade.draw_text("Appuyer sur 'Espace' pour commencer une nouvelle partie", 491, 50, arcade.color.DOLLAR_BILL, 25, width=1024)


    def on_draw(self):
        self.player.center_x = 400
        self.player.center_y = 600
        self.computer.center_x = 1450
        self.computer.center_y = 600

        arcade.start_render()

        arcade.draw_text(SCREEN_TITLE, 550, 900, arcade.color.DARK_ELECTRIC_BLUE, 60, width=1024)
        self.draw_instructions()
        self.player.draw()
        self.computer.draw()
        self.draw_possible_attack()
        self.draw_computer_attack()
        self.draw_scores()

    def on_update(self, delta_time):
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update(delta_time)
            self.paper.on_update(delta_time)
            self.scissors.on_update(delta_time)

        if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen == True:
            if self.computer_attack == 0:
                self.computer_attack_type = AttackType.ROCK
            elif self.computer_attack == 1:
                self.computer_attack_type = AttackType.PAPER
            elif self.computer_attack == 2:
                self.computer_attack_type = AttackType.SCISSORS
            self.game_state = GameState.ROUND_DONE
            self.validate_victory()
            if self.player_score == 3 or self.computer_score == 3:
                self.game_state = GameState.GAME_OVER

    def on_key_press(self, key, key_modifiers):
        if self.game_state == GameState.NOT_STARTED:
            if key == 32:
                self.game_state = GameState.ROUND_ACTIVE
        if self.game_state == GameState.ROUND_DONE:
            if key == 32:
                self.game_state = GameState.ROUND_ACTIVE
                self.player_attack_chosen = False
                self.player_won_round = None
                self.draw_round = None
                self.computer_attack = random.randint(0, 2)
        if self.game_state == GameState.GAME_OVER:
            if key == 32:
                self.reset_round()
                self.game_state = GameState.NOT_STARTED

    def reset_round(self):
        self.computer_attack = random.randint(0, 2)
        self.player_attack_chosen = False
        self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}
        self.player_won_round = None
        self.draw_round = None
        self.player_score = 0
        self.computer_score = 0

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x, y)):
                self.player_attack_type = AttackType.ROCK
                self.player_attack_chosen = True

            if self.paper.collides_with_point((x, y)):
                self.player_attack_type = AttackType.PAPER
                self.player_attack_chosen = True

            if self.scissors.collides_with_point((x, y)):
                self.player_attack_type = AttackType.SCISSORS
                self.player_attack_chosen = True

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
