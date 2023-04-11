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
    
    def do_move(self, move):
        for dice in move:
            self.save_dice(dice)
        self.turns_played += 1
    
    def save_dice(self, dice):
        self.saved_dice.append(dice)

    def get_dice_saved_number(self):
        return len(self.saved_dice)
    
    def get_legal_moves(self):
        if self.turns_played == 2:
            # last turn, the only legal move is to save all dice
            return [self.rolled_dice.copy()]
        moves = []
        # legal moves are all subsets of rolled_dice
        for i in range(2 ** len(self.rolled_dice)):
            move = []
            for j in range(len(self.rolled_dice)):
                if (i >> j) % 2 == 1:
                    move.append(self.rolled_dice[j])
            moves.append(move)
        return moves
    
    def copy(self):
        return Player(self.hp, self.rolled_dice.copy(), self.saved_dice.copy(), self.turns_played)

class Game():
    def __init__(self, player1=Player(), player2=Player(), current_player=0):
        self.current_player = current_player
        self.players = (player1, player2)

    def winner(self):
        if self.players[0].hp <= 0:
            return 1
        if self.players[1].hp <= 0:
            return 0
        return -1
    
    def get_legal_moves(self):
        return self.players[self.current_player].get_legal_moves()
    
    def roll_dice(self):
        self.players[self.current_player].roll_dice()
    
    def do_move(self, move):
        self.players[self.current_player].do_move(move)

    def end_turn(self):
        if self.players[0].turns_played == 3 and self.players[1].turns_played == 3:
            # both players have played 3 turns, it's time to calculate the hp loss
            for player in [0,1]:
                for dice in self.players[player].saved_dice:
                    if dice == 'Arrow':
                        if 'Shield' in self.players[1 - player].saved_dice:
                            self.players[1 - player].saved_dice.remove('Shield')
                        else:
                            self.players[1 - player].hp -= 1
                    elif dice == 'Axe':
                        if 'Helmet' in self.players[1 - player].saved_dice:
                            self.players[1 - player].saved_dice.remove('Helmet')
                        else:
                            self.players[1 - player].hp -= 1
            # reset the game
            self.players[0].saved_dice = []
            self.players[1].saved_dice = []
            self.players[0].rolled_dice = []
            self.players[1].rolled_dice = []
            self.players[0].turns_played = 0
            self.players[1].turns_played = 0
        else:
            self.players[self.current_player].rolled_dice = []
            # switch the current player
            self.current_player = 1 - self.current_player

    def __str__(self):
        return f'Game with players:\n{self.players[0]}\n{self.players[1]}'
    
    def is_over(self):
        return self.winner() != -1
    
    def get_state(self):
        # doesn't include players' hp neither the turns played
        return (tuple(self.players[0].saved_dice), tuple(self.players[1].saved_dice))
    
    def get_current_player(self):
        return self.current_player

    def copy(self):
        return Game(self.players[0].copy(), self.players[1].copy(), self.current_player)

if __name__ == '__main__':
    game = Game()
    for _ in range(6):
        print(game)
        game.roll_dice()
        move = random.choice(game.get_legal_moves())
        game.do_move(move)
        print(f'\nPlayer {game.get_current_player()} plays {move}')
        game.end_turn()
        print()
        print()
    print(game)

        

