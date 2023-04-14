from customtkinter import *

class SettingsView(CTkFrame):
    def __init__(self, app):
        super().__init__(master=app, fg_color="green")
        self.app = app
        
        # Create a label widget
        self.lbl = CTkLabel(self, text="Settings view!")
        self.lbl.pack()

        # Create a button widget
        self.btn = CTkButton(self, text="Switch to game view", command=self.switch_view)
        self.btn.pack()

    def switch_view(self):
        self.destroy()
        self.app.show_game()

class GameView(CTkFrame):
    def __init__(self, app):
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

        # Set up the main window
        self.title("MCTS Orlog")
        self.geometry("1200x600")

        # Show the first frame
        self.show_settings()

    def show_settings(self):
        SettingsView(app=self).pack(expand=True, fill="both")

    def show_game(self):
        GameView(app=self).pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()
