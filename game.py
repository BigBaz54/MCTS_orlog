import random


class Player():
    def __init__(self, hp=15, rolled_dice=None, saved_dice=None, turns_played=0):
        if saved_dice is None:
            saved_dice = []
        if rolled_dice is None:
            rolled_dice = []
        self.hp = hp
        self.rolled_dice = rolled_dice
        self.saved_dice = saved_dice
        self.turns_played = turns_played

    def __str__(self):
        return f'\nPlayer with {self.hp} HP\nSaved dice : {self.saved_dice}\nTurns played : {self.turns_played}'
    
    def roll_dice(self):
        rolled_dice = []
        remaining_dice = 6 - self.get_dice_saved_number()
        for _ in range(remaining_dice):
            d = random.randint(1, 6)
            if d <= 2:
                rolled_dice.append('Axe')
            elif d <= 4:
                rolled_dice.append('Arrow')
            elif d <= 5:
                rolled_dice.append('Shield')
            else:
                rolled_dice.append('Helmet')
        self.rolled_dice = rolled_dice
    
    def random_move(self):
        if (self.turns_played == 2):
            # last turn, save all dice
            for d in self.rolled_dice:
                self.save_dice(d)
        else:
            for d in self.rolled_dice:
                if (random.random() < 0.5):
                    self.save_dice(d)
    
    def save_dice(self, dice):
        self.saved_dice.append(dice)

    def get_dice_saved_number(self):
        return len(self.saved_dice)
    
    def random_turn(self):
        self.roll_dice()
        self.random_move()
        self.turns_played += 1

class Game():
    def __init__(self, player1=Player(), player2=Player()):
        self.current_player = 0
        self.players = [player1, player2]




if __name__ == '__main__':
    game = Game()
    for __ in range(3):
        game.players[0].random_turn()
        game.players[1].random_turn()
        print(game.players[0])
        print(game.players[1])
