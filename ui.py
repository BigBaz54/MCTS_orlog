import random
from customtkinter import *
import tkinter as tk
from PIL import Image
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
        hp = self.hp_entry.get()
        reroll = self.reroll_entry.get()
        exp = self.exp_entry.get()
        games = self.games_entry.get()
        time = self.time_entry.get()
        self.destroy()
        new_game = game.Game(max_hp=int(hp or 15), max_rerolls=int(reroll or 3), current_player=random.randint(0, 1))
        bot = monte_carlo.MonteCarlo(new_game, exploration_param=float(exp or 1.4), max_simulations=int(games or 1000), max_time_seconds=float(time or 5))
        self.app.show_game(new_game, bot)

class GameView(CTkFrame):
    def __init__(self, app, game, bot):
        super().__init__(master=app)
        self.app = app
        self.game = game
        self.bot = bot
        self.rolled_dice = []
        self.rolled_dice_buttons = []
        # list of 0 or 1, 1 if the dice is selected
        self.selected_dice = []
        self.player_dice_buttons = []
        self.bot_dice_buttons = []

        self.arrow_img = CTkImage(Image.open('assets/img/arrow.png'), size=(75, 75))
        self.helmet_img = CTkImage(Image.open('assets/img/helmet.png'), size=(75, 75))
        self.axe_img = CTkImage(Image.open('assets/img/axe.png'), size=(75, 75))
        self.shield_img = CTkImage(Image.open('assets/img/shield.png'), size=(75, 75))
        self.little_arrow_img = CTkImage(Image.open('assets/img/arrow.png'), size=(30, 30))
        self.little_helmet_img = CTkImage(Image.open('assets/img/helmet.png'), size=(30, 30))
        self.little_axe_img = CTkImage(Image.open('assets/img/axe.png'), size=(30, 30))
        self.little_shield_img = CTkImage(Image.open('assets/img/shield.png'), size=(30, 30))

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
        self.games_var = tk.StringVar(value="Games simulated: ")
        self.games_label = CTkLabel(self.right_frame, textvariable=self.games_var, font=('Helvetica', 15))
        self.games_label.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        self.time_var = tk.StringVar(value="Search time: s")
        self.time_label = CTkLabel(self.right_frame, textvariable=self.time_var, font=('Helvetica', 15))
        self.time_label.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        # scrollable frame to display the moves and their informations
        self.scrollable_frame = CTkScrollableFrame(self.right_frame, width=400, height=400)
        self.scrollable_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10, padx=15)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.nb_moves_var = tk.StringVar(value=" legal moves:")
        self.nb_moves_label = CTkLabel(self.scrollable_frame, textvariable=self.nb_moves_var, font=('Helvetica', 15))
        self.nb_moves_label.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
        self.moves_var = tk.StringVar(value="('Arrow', 'Arrow', 'Arrow', 'Axe', 'Axe', 'Helmet'): 26.32% (5 / 19)\nteydfga\nazery\ntestaryzt\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\ntest\nteydfga\nazery\n")
        self.moves_label = CTkLabel(self.scrollable_frame, textvariable=self.moves_var, font=('Helvetica', 13), justify="left")
        self.moves_label.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        # results of the search
        self.depth_var = tk.StringVar(value="Average depth: ")
        self.depth_label = CTkLabel(self.right_frame, textvariable=self.depth_var, font=('Helvetica', 15))
        self.depth_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10,5), padx=50)

        self.move_var = tk.StringVar(value="Move selected: ")
        self.move_label = CTkLabel(self.right_frame, textvariable=self.move_var, font=('Helvetica', 15))
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
        self.turn_player_var = tk.StringVar(value="Turn 1: "+("Player" if self.game.current_player == 0 else "Bot"))
        self.turn_label = CTkLabel(self.left_frame, textvariable=self.turn_player_var, font=('Helvetica', 25))
        self.turn_label.grid(row=1, column=0, columnspan=2, pady=(50, 20))

        # rolled dice frame
        self.rolled_dice_frame = CTkFrame(self.left_frame)
        self.rolled_dice_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5, padx=10)
        self.rolled_dice_frame.grid_columnconfigure(0, weight=1)
        self.rolled_dice_frame.grid_columnconfigure(7, weight=1)

        self.rolled_dice_label = CTkLabel(self.rolled_dice_frame, text="Rolled dice:", font=('Helvetica', 20))
        self.rolled_dice_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=(20,0), padx=5)

        # label to set heigth of the frame
        CTkLabel(self.rolled_dice_frame, text="", height=170).grid(row=1, column=0, sticky="nsew")

        # confirm/roll button
        self.confirm_roll_button = CTkButton(self.left_frame, text="Start", width=40, font=('Helvetica', 30), command=self.start)
        self.confirm_roll_button.grid(row=3, column=0, columnspan=2, pady=35)

        # player's info
        self.player_frame = CTkFrame(self.left_frame)
        self.player_frame.grid(row=4, column=0, sticky="nsew", pady=5, padx=5)
        self.player_frame.grid_columnconfigure(0, weight=1)
        self.player_frame.grid_columnconfigure(7, weight=1)

        self.player_hp_var = tk.StringVar(value="Player HP: "+str(self.game.players[0].hp))
        self.player_hp_label = CTkLabel(self.player_frame, textvariable=self.player_hp_var, font=('Helvetica', 18), width=250)
        self.player_hp_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=5, padx=5)

        # label to set heigth of the frame
        CTkLabel(self.player_frame, text="", height=100).grid(row=1, column=0, sticky="nsew")

        # bot's info
        self.bot_frame = CTkFrame(self.left_frame)
        self.bot_frame.grid(row=4, column=1, sticky="nsew", pady=5, padx=5)
        self.bot_frame.grid_columnconfigure(0, weight=1)
        self.bot_frame.grid_columnconfigure(7, weight=1)

        # label to set heigth of the frame
        CTkLabel(self.bot_frame, text="", height=100).grid(row=1, column=0, sticky="nsew")

        self.bot_hp_var = tk.StringVar(value="Bot HP: "+str(self.game.players[1].hp))
        self.bot_hp_label = CTkLabel(self.bot_frame, textvariable=self.bot_hp_var, font=('Helvetica', 18), width=250)
        self.bot_hp_label.grid(row=0, column=0, columnspan=8, sticky="nsew", pady=5, padx=5)
        
    def start(self):
        if (self.game.current_player==1):
            self.do_bot_turn()
        else:
            self.confirm_roll_button.configure(text="Roll dice")
            self.confirm_roll_button.configure(command=self.roll_dice)

    def switch_view(self):
        self.destroy()
        self.app.show_settings()

    def roll_dice(self):
        self.game.roll_dice()
        self.rolled_dice = self.game.players[self.game.current_player].rolled_dice
        self.update_rolled_dice()
        if (self.game.current_player==0):
            self.confirm_roll_button.configure(text="Confirm")
            self.confirm_roll_button.configure(command=self.confirm)
        else:
            self.confirm_roll_button.configure(text="Ok")
            self.confirm_roll_button.configure(command=self.confirm)
    
    def update_rolled_dice(self):
        for e in (self.rolled_dice_buttons):
            e.destroy()
        self.rolled_dice_buttons = []
        for i in range(len(self.rolled_dice)):
            if (self.rolled_dice[i]=="Arrow"):
                img = self.arrow_img
            elif (self.rolled_dice[i]=="Axe"):
                img = self.axe_img
            elif (self.rolled_dice[i]=="Shield"):
                img = self.shield_img
            elif (self.rolled_dice[i]=="Helmet"):
                img = self.helmet_img
            self.rolled_dice_buttons.append(CTkButton(self.rolled_dice_frame, text="", image=img, width=75, height=75, fg_color="#eeeee4", border_color="#ff7575", hover_color="#c9c9c3", border_width=3, command=lambda i=i: self.toggle_dice(i)))
            self.rolled_dice_buttons[i].grid(row=1, column=i+1, pady=5, padx=5)
            self.selected_dice.append(0)

    def confirm(self):
        move = []
        for i in range(len(self.selected_dice)):
            if (self.selected_dice[i]==1):
                move.append(self.rolled_dice[i])
        self.play_move(move)
        self.end_turn()

    def play_move(self, move):
        self.game.do_move(move)
        self.update_saved_dice()


    def end_turn(self):
        self.game.end_turn()
        self.player_hp_var.set("Player HP: " + str(self.game.players[0].hp))
        self.bot_hp_var.set("Bot HP: " + str(self.game.players[1].hp))
        self.turn_player_var.set(f"Turn {self.game.players[self.game.current_player].turns_played+1}: {'Player' if (self.game.current_player==0) else 'Bot'}")
        self.rolled_dice = []
        self.selected_dice = []
        self.update_rolled_dice()
        self.update_saved_dice()
        if (self.game.current_player==1 or self.game.players[0].turns_played==2):
            self.do_bot_turn()
        else:
            self.confirm_roll_button.configure(text="Roll Dice")
            self.confirm_roll_button.configure(command=self.roll_dice)

    def do_bot_turn(self):
        self.roll_dice()
        # disable all buttons during bot turn
        for e in (self.rolled_dice_buttons):
            e.configure(state="disabled")
        bot_move = self.bot.get_best_move()

        # display the move selected by the bot
        for e in (bot_move):
            for but in (self.rolled_dice_buttons):
                if (self.selected_dice[self.rolled_dice_buttons.index(but)]==0):
                    if (but.cget("image")==self.arrow_img and e=="Arrow" or but.cget("image")==self.axe_img and e=="Axe" or but.cget("image")==self.shield_img and e=="Shield" or but.cget("image")==self.helmet_img and e=="Helmet"):
                        self.toggle_dice(self.rolled_dice_buttons.index(but))
                        break

    def toggle_dice(self, i):
        if (self.selected_dice[i]==1):
            self.selected_dice[i] = 0
            self.rolled_dice_buttons[i].configure(border_color="#ff7575")
        else:
            self.selected_dice[i] = 1
            self.rolled_dice_buttons[i].configure(border_color="#9fff75")

    def update_saved_dice(self):
        player_dice = self.game.players[0].saved_dice
        bot_dice = self.game.players[1].saved_dice
        for e in (self.player_dice_buttons):
            e.destroy()
        for e in (self.bot_dice_buttons):
            e.destroy()
        self.player_dice_buttons = []
        self.bot_dice_buttons = []
        for i in range(len(player_dice)):
            if (player_dice[i]=="Arrow"):
                img = self.little_arrow_img
            elif (player_dice[i]=="Axe"):
                img = self.little_axe_img
            elif (player_dice[i]=="Shield"):
                img = self.little_shield_img
            elif (player_dice[i]=="Helmet"):
                img = self.little_helmet_img
            self.player_dice_buttons.append(CTkButton(self.player_frame, text="", image=img, width=30, height=30, fg_color="#eeeee4", hover_color="#eeeee4"))
            self.player_dice_buttons[i].grid(row=1, column=i+1, pady=5, padx=5)
        for i in range(len(bot_dice)):
            if (bot_dice[i]=="Arrow"):
                img = self.little_arrow_img
            elif (bot_dice[i]=="Axe"):
                img = self.little_axe_img
            elif (bot_dice[i]=="Shield"):
                img = self.little_shield_img
            elif (bot_dice[i]=="Helmet"):
                img = self.little_helmet_img
            self.bot_dice_buttons.append(CTkButton(self.bot_frame, text="", image=img, width=30, height=30, fg_color="#eeeee4", hover_color="#eeeee4"))
            self.bot_dice_buttons[i].grid(row=1, column=i+1, pady=5, padx=5)

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
