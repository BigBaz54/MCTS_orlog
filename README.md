# MCTS_orlog
The goal of this project is to implement Monte Carlo Tree Search to find the best move in a simplified version of the Orlog dice game from Assassin's Creed.

## How to run the code
To run the code, you need to have python 3 installed on your computer.
You also need to install the following python libraries:
  - tkinter
  - customtkinter (v5.1.2 or newer, you can install the last version with ```pip install "git+https://github.com/TomSchimansky/CustomTkinter.git"```)
  - Pillow

Then, you can run the code by typing the following command in the terminal:
```
python3 ui.py
```

## How to use the interface
The interface has 2 views.

### Settings view
<img src="https://user-images.githubusercontent.com/96493391/232820636-65810bcd-52fa-4f84-98f5-d9429795ae16.png" width="312" height="310">

The settings view allows you to change the game settings and the parameters of the Monte Carlo Tree Search.

All inputs are optionnal and the default values are displayed within placeholders.


### Game view
<img src="https://user-images.githubusercontent.com/96493391/232825372-67eed57e-216b-42fd-8eec-53eb1f72f2a4.png" width="750" height="377">

The right part is the bot panel. It displays :
  - the number of simulations run to select the best move
  - the time it has taken
  - the list of all the legal moves in this state, their win rate and the number of simulations that started with this move
  - the average depth of the end of the simulations 
  - the move selected at the end of the search.


The left part is the game :

When it's your turn, you can click on "Roll dice" to roll the dice and then click on the dice you want to save. Once you have selected your dice, you can click on "Confirm". If it's your last turn, you have no choice but to save all the dice so all you have to do is to click on "Confirm".

When it's the bot's turn, the selected move is displayed and you can click on "Ok" once you have acknowledged it.

Each player's health points and saved dice are displayed at the bottom of the panel.
