from customtkinter import *
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
        game = game.Game()
        self.app.show_game(game)

class GameView(CTkFrame):
    def __init__(self, app, game):
        super().__init__(master=app)
        self.app = app

        self.left_frame = CTkFrame(master=self, fg_color="lightblue")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = CTkFrame(master=self, fg_color="purple")
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # Create a label widget
        self.lbl = CTkLabel(self.left_frame, text="Game view!")
        self.lbl.pack()

        # Create a button widget
        self.btn = CTkButton(self.left_frame, text="Switch to settings view", command=self.switch_view)
        self.btn.pack()

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

    def show_game(self, game):
        self.center_window(1200, 600)
        GameView(app=self, game=game).pack(expand=True, fill="both")

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
