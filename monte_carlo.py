import time


class MonteCarlo():
    def __init__(self, game, max_time_seconds=1):
        self.game = game
        self.states = []
        self.max_time_seconds = max_time_seconds
        # dictionaries of states with their win and play counts
        self.played = {}
        self.won = {}

    def update(self, state):
        self.states.append(state)

    def get_best_move(self):
        begin = time.time()
        while time.time() - begin < self.max_time_seconds:
            self.run_simulation()

    def run_simulation(self):
        pass
