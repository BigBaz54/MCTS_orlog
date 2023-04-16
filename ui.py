from customtkinter import *
import tkinter as tk
import monte_carlo
import game

class SettingsView(CTkFrame):
    def __init__(self, app):
        super().__init__(master=app)
        self.app = app

        self.grid_configure(column=6, row=9)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        
        self.gs_label = CTkLabel(self, text="Game settings", font=('Helvetica', 18))
        self.gs_label.grid(row=1, column=1, columnspan=4, pady=(30,10))

        self.hp_label = CTkLabel(self, text="Max HP", font=('Helvetica', 15))
        self.hp_label.grid(row=2, column=1, sticky="e", pady=5, padx=5)
        self.hp_entry = CTkEntry(self, placeholder_text="15", width=35, justify="center")
        self.hp_entry.grid(row=2, column=2, sticky="w", padx=5)

        self.reroll_label = CTkLabel(self, text="Max reroll", font=('Helvetica', 15))
        self.reroll_label.grid(row=2, column=3, sticky="e", pady=5, padx=5)
        self.reroll_entry = CTkEntry(self, placeholder_text="3", width=30, justify="center")
        self.reroll_entry.grid(row=2, column=4, sticky="w", padx=(5,50))

        self.ms_label = CTkLabel(self, text="MCTS settings", font=('Helvetica', 18))
        self.ms_label.grid(row=3, column=1, columnspan=4, pady=(30,10))

        self.exp_label = CTkLabel(self, text="Exploration param.", font=('Helvetica', 15))
        self.exp_label.grid(row=4, column=1, columnspan=2, sticky="e", pady=5, padx=(60, 5))
        self.exp_entry = CTkEntry(self, placeholder_text="1.4", width=40, justify="center")
        self.exp_entry.grid(row=4, column=3, columnspan=2, padx=5)

        self.games_label = CTkLabel(self, text="Max games simulated", font=('Helvetica', 15))
        self.games_label.grid(row=5, column=1, columnspan=2, sticky="e", pady=5, padx=5)
        self.games_entry = CTkEntry(self, placeholder_text="1000", width=50, justify="center")
        self.games_entry.grid(row=5, column=3, columnspan=2, padx=5)

        self.time_label = CTkLabel(self, text="Max search time (s)", font=('Helvetica', 15))
        self.time_label.grid(row=6, column=1, columnspan=2, sticky="e", pady=5, padx=5)
        self.time_entry = CTkEntry(self, placeholder_text="5", width=30, justify="center")
        self.time_entry.grid(row=6, column=3, columnspan=2, padx=5)

        self.play_btn = CTkButton(self, text="Play !", command=self.switch_view, font=('Helvetica', 20))
        self.play_btn.grid(row=7, column=1, columnspan=4, pady=(30,30), ipady=10)

    def switch_view(self):
        self.destroy()
        new_game = game.Game(max_hp=int(self.hp_entry.get() or 15), max_rerolls=int(self.reroll_entry.get() or 3))
        bot = monte_carlo.MonteCarlo(new_game, exploration_param=float(self.exp_entry.get() or 1.4), max_simulations=int(self.games_entry.get() or 1000), max_time_seconds=float(self.time_entry.get() or 5))
        self.app.show_game(new_game, bot)

class GameView(CTkFrame):
    def __init__(self, app, game, bot):
        super().__init__(master=app)
        self.app = app
        self.game = game
        self.bot = bot

        # configure main grid to have the left panel (game) and the right panel (bot)
        self.grid_configure(column=2, row=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # right panel
        self.right_frame = CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(5, weight=1)

        # informations about the search
        self.games_var = tk.StringVar()
        self.games_label = CTkLabel(self.right_frame, text="Games simulated: "+self.games_var.get(), font=('Helvetica', 15))
        self.games_label.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        self.time_var = tk.StringVar()
        self.time_label = CTkLabel(self.right_frame, text="Search time: "+self.time_var.get()+"s", font=('Helvetica', 15))
        self.time_label.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        # scrollable frame to display the moves and their informations
        self.scrollable_frame = CTkScrollableFrame(self.right_frame, width=400, height=400)
        self.scrollable_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10, padx=15)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.nb_moves_var = tk.StringVar()
        self.nb_moves_label = CTkLabel(self.scrollable_frame, text=self.nb_moves_var.get()+" legal moves:", font=('Helvetica', 15))
        self.nb_moves_label.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
        self.moves_var = tk.StringVar(value="('Arrow', 'Arrow', 'Arrow', 'Axe', 'Axe', 'Helmet'): 26.32% (5 / 19)\nteydfga\nazery\ntestaryzt\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\n")
        self.moves_label = CTkLabel(self.scrollable_frame, text=self.moves_var.get(), font=('Helvetica', 13), justify="left")
        self.moves_label.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        # results of the search
        self.depth_var = tk.StringVar()
        self.depth_label = CTkLabel(self.right_frame, text="Average depth: "+self.depth_var.get(), font=('Helvetica', 15))
        self.depth_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10,5), padx=50)

        self.move_var = tk.StringVar()
        self.move_label = CTkLabel(self.right_frame, text="Move selected: "+self.move_var.get(), font=('Helvetica', 15))
        self.move_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=5, padx=50)

        # left panel
        self.left_frame = CTkFrame(master=self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(5, weight=1)

        # new game button
        self.new_game_button = CTkButton(self.left_frame, text="New game", command=self.switch_view, width=40, font=('Helvetica', 15))
        self.new_game_button.place(x=5, y=5, anchor="nw")

        # turn label
        self.turn_var = tk.StringVar()
        self.player_var = tk.StringVar()
        self.turn_label = CTkLabel(self.left_frame, text=f"Turn {self.turn_var.get()}: {self.player_var.get()}", font=('Helvetica', 15))
        self.turn_label.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        # rolled dice frame
        self.rolled_dice_frame = CTkFrame(self.left_frame)
        self.rolled_dice_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5, padx=50)
        self.rolled_dice_frame.grid_columnconfigure(0, weight=1)
        self.rolled_dice_frame.grid_columnconfigure(7, weight=1)

        self.rolled_dice_label = CTkLabel(self.rolled_dice_frame, text="Rolled dice:", font=('Helvetica', 15))
        self.rolled_dice_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=5, padx=5)

        # temp dice buttons
        CTkButton(self.rolled_dice_frame, text="1", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=1, pady=5, padx=5)
        CTkButton(self.rolled_dice_frame, text="2", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=2, pady=5, padx=5)
        CTkButton(self.rolled_dice_frame, text="3", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=3, pady=5, padx=5)
        CTkButton(self.rolled_dice_frame, text="4", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=4, pady=5, padx=5)
        CTkButton(self.rolled_dice_frame, text="5", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=5, pady=5, padx=5)
        CTkButton(self.rolled_dice_frame, text="6", width=75, height=75, font=('Helvetica', 15)).grid(row=1, column=6, pady=5, padx=5)

        # confirm/roll button
        self.confirm_roll_var = tk.StringVar(value="Roll dice")
        self.confirm_roll_button = CTkButton(self.left_frame, text=self.confirm_roll_var.get(), width=40, font=('Helvetica', 20))
        self.confirm_roll_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

        # player's info
        self.player_frame = CTkFrame(self.left_frame)
        self.player_frame.grid(row=4, column=0, sticky="nsew", pady=5, padx=5)
        self.player_frame.grid_columnconfigure(0, weight=1)
        self.player_frame.grid_columnconfigure(7, weight=1)

        self.player_hp_var = tk.StringVar()
        self.player_hp_label = CTkLabel(self.player_frame, text="HP: "+self.player_hp_var.get(), font=('Helvetica', 15))
        self.player_hp_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=5, padx=5)

        CTkButton(self.player_frame, text="1", width=50, height=50, font=('Helvetica', 15), state="disabled").grid(row=1, column=1, pady=5, padx=5)
        CTkButton(self.player_frame, text="2", width=50, height=50, font=('Helvetica', 15), state="disabled").grid(row=1, column=2, pady=5, padx=5)
        CTkButton(self.player_frame, text="3", width=50, height=50, font=('Helvetica', 15), state="disabled").grid(row=1, column=3, pady=5, padx=5)

        # bot's info
        self.bot_frame = CTkFrame(self.left_frame)
        self.bot_frame.grid(row=4, column=1, sticky="nsew", pady=5, padx=5)
        self.bot_frame.grid_columnconfigure(0, weight=1)
        self.bot_frame.grid_columnconfigure(7, weight=1)

        self.bot_hp_var = tk.StringVar()
        self.bot_hp_label = CTkLabel(self.bot_frame, text="HP: "+self.bot_hp_var.get(), font=('Helvetica', 15))
        self.bot_hp_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=5, padx=5)

        CTkButton(self.bot_frame, text="1", width=50, height=50, font=('Helvetica', 15), state="disabled").grid(row=1, column=1, pady=5, padx=5)
        CTkButton(self.bot_frame, text="2", width=50, height=50, font=('Helvetica', 15), state="disabled").grid(row=1, column=2, pady=5, padx=5)




        

    def switch_view(self):
        self.destroy()
        self.app.show_settings()

class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        # Set up the main window
        self.title("MCTS Orlog")
        self.resizable(False, False)

        # Show the first frame
        self.show_settings()

    def show_settings(self):
        self.center_window(500, 500)
        SettingsView(app=self).place(relx=0.5, rely=0.5, anchor="center")

    def show_game(self, game, bot):
        self.center_window(1200, 600)
        GameView(app=self, game=game, bot=bot).place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def center_window(self, w, h):
        # resize the window and center it on the screen
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

if __name__ == "__main__":
    app = App()
    app.mainloop()
