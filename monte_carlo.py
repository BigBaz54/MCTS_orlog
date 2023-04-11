import random
import time
from math import log, sqrt


class MonteCarlo():
    def __init__(self, game, max_time_seconds=1, exploration_param=1.4):
        self.game = game
        # the greater the exploration parameter, the more the algorithm will favor unexplored moves
        self.exploration_param = exploration_param
        self.states = []
        self.max_time_seconds = max_time_seconds
        # dictionaries of states with their win and play counts
        self.played = {}
        self.won = {}

    def get_best_move(self):
        self.max_depth = 0
        player = self.game.get_current_player()
        print("Player to play", player)
        legal_moves = self.game.get_legal_moves()
        print("Possible moves:", len(legal_moves))
        # if no real choice to make
        if not legal_moves:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        games = 0
        begin = time.time()
        while time.time() - begin < self.max_time_seconds:
            self.run_simulation()
            games += 1

        # list of (move, state) tuples
        # for all legal moves and their resulting game states
        moves_states = []
        for move in legal_moves:
            # copy the game so that the original is not changed
            game_copy = self.game.copy()
            game_copy.do_move(move)
            state = game_copy.get_state()
            moves_states.append((move, state))

        # pick the move with the highest winrate, if there are multiple, pick randomly
        winrates_moves = [(self.won.get((player, state), 0) / self.played.get((player, state), 1), move) for move, state in moves_states]
        max_winrate = max(winrates_moves)[0]
        print("Best winrate:", max_winrate)
        best_moves = [move for winrate, move in winrates_moves if winrate == max_winrate]
        print("Best moves:", best_moves)
        best_move = random.choice(best_moves)

        # display the stats for each possible play
        for x in sorted(
            ((100 * self.won.get((player, s), 0) / self.played.get((player, s), 1),
              self.won.get((player, s), 0),
              self.played.get((player, s), 0),
              m)
             for m, s in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return best_move

    def run_simulation(self):
        played, won = self.played, self.won
        depth = 0
        game = self.game.copy()
        visited_states = set()
        expand = True
        move_num = 0
        while not game.is_over() and move_num < 10000:
            move_num += 1
            depth+=1
            player = game.get_current_player()
            legal_moves = game.get_legal_moves()

            moves_states = []
            for move in legal_moves:
                game_copy = game.copy()
                game_copy.do_move(move)
                state = game_copy.get_state()
                moves_states.append((move, state))
            
            if all(played.get((player, state)) for move, state in moves_states):
                # if we have stats on all of the legal moves here, use them to compute UCB1
                log_total = log(
                    sum(played[(player, state)] for move, state in moves_states)
                )
                max_value = max(
                    ((won[(player, state)] / played[(player, state)]) +
                     self.exploration_param * sqrt(log_total / played[(player, state)]), move, state)
                    for move, state in moves_states
                )[0]
                # pick one of the moves with the highest upper confidence bound
                greatest_UCB_moves_states = [move_state for move_state in moves_states 
                                             if ((won[(player, move_state[1])] / played[(player, move_state[1])]) +self.exploration_param * sqrt(log_total / played[(player, move_state[1])])) 
                                             == max_value]
                move, state = random.choice(greatest_UCB_moves_states)
            else:
                # otherwise, just make an arbitrary decision
                move, state = random.choice(moves_states)

            # player refers to the player who made the move leading to the state
            if expand and (player, state) not in played:
                expand = False
                played[(player, state)] = 0
                won[(player, state)] = 0
                if depth > self.max_depth:
                    self.max_depth = depth

            visited_states.add((player, state))
            game.do_move(move)
            game.end_turn()
            game.roll_dice()

        # backpropagation
        for player, state in visited_states:
            if (player, state) not in played:
                continue
            played[(player, state)] += 1
            if game.winner() == player:
                won[(player, state)] += 1

if __name__ == "__main__":
    import game

    # play a game between two monte carlo bots
    g = game.Game()
    bot = MonteCarlo(g, max_time_seconds=5, exploration_param=1.4)
    while not g.is_over():
        g.players[g.current_player].roll_dice()
        
        print("Thinking...")
        move = bot.get_best_move()
        print("Playing", move)
        g.do_move(move)
        g.end_turn()
        print("Player 0:", g.players[0].hp)
        print("Player 1:", g.players[1].hp)
        print()