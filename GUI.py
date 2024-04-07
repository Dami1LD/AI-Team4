import tkinter as tk
from tkinter import ttk
import random

import with_graphs

Tree = with_graphs.Graph()
original_number = 0
default_starter = "User"
selected_number = 0
selected_number_str = "0"
actual_state = None
choosen_algo = "Minimax"


# GUI for the game of divide me 
root = tk.Tk()
root.title("TEAM 4 AI")

#functions
def start_game(num):
    """function for starting the game."""
    if num != '':
        global Tree, actual_state
        if default_starter == "User":
            Tree = with_graphs.Graph()
            startState = with_graphs.State(int(num), 0, 0, 0, 1)
            Tree = with_graphs.generate_graph(startState, 1, Tree)
        else:
            Tree = with_graphs.Graph()
            startState = with_graphs.State(int(num), 0, 0, 0, 2)
            Tree = with_graphs.generate_graph(startState, 1, Tree)
        actual_state = startState
    
    #create_game_board_labels(root)
    create_gui(root)
    print("Game started with the number: ", num)

def make_move(divider):
    """ function for making move (dividing the selected number with (2/3/4)) in the game."""
    global actual_state
    selected_number = int(divider)  # Mise à jour de selected_number avec le diviseur sélectionné
    print("Selected number: ", selected_number)
    print(int(divider))
    actual_state = Tree.get_from_divisor(actual_state, int(divider))




def start_new_game():
    """ function for starting a new game when either after the game ends or the user wants to restart the game."""
    global Tree, original_number, default_starter, selected_number, actual_state, choosen_algo
    Tree = with_graphs.Graph()
    original_number = 0
    default_starter = "User"
    selected_number = 0
    selected_number_str = "0"
    actual_state = None
    choosen_algo = "Minimax"

def choose_algorithm():
    """ function for choosing the algorithm either minimax or the alpha-beta algorithm."""
    pass

def generate_numbers():
    """
    Generate 5 random numbers in the range of 20000 and 30000 which divisible by 2 and 3 and 4 (2*3*4=12).

    Returns:
    list: 5 random numbers divisible by 2 and 3 and 4 (2*3*4=12).
    """
    divisible_numbers = []
    while len(divisible_numbers) < 5:
        num = random.randint(20000, 30000)
        if num % 12 == 0:
            divisible_numbers.append(num)
    return divisible_numbers

#starting to create the GUI FOR THE DIVIDE ME! 
def create_gui(root):
    global original_number
    # Setting the window's position
    set_window_centered(root)
    # disabling the maximization of the page 
    root.resizable(False, False)
    # Set lime green as background color
    root.configure(background='lime green')
    #Will be defined later in below
    create_title(root)
    create_options_section(root)
    create_game_board(root)
    create_divider_selection(root)
    #creating custom styles for the desired font for the buttons like user, computer, make move, start game etc.
    custom_style = ttk.Style()
    custom_style.configure("Custom.TButton", font=("Comic Sans MS", 12))
    custom_style.configure("Custom.TRadiobutton", font=("Comic Sans MS", 10)) 
    root.mainloop()

def set_window_centered(root):    
    # sizing up the width and height of the laptop screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    #setting the windows of the game to the center of the screen
    # inorder to center the window it calculates x and y coordinates first
    x = (screen_width - root.winfo_reqwidth()) / 2
    y = (screen_height - root.winfo_reqheight()) / 2
    root.geometry("+{}+{}".format(int(x), int(y)))
    
def create_title(root):
    #cREATING the title label of the GUI giving the font and the color of this label
    title_label = ttk.Label(root, text="DIVIDE ME!", font=("Comic Sans MS", 24, "bold"), foreground="dark blue")
    title_label.grid(row=0, column=0, pady=10, padx=(230, 180), sticky="w")

def create_options_section(root):
#HERE IS THE OPTIONS ARE A WHERE WE CAN SELECT THE PLAYER /ALGORITHM
    options_frame = ttk.Frame(root)
    options_frame.grid(row=1, column=0)

    create_who_starts_section(options_frame)
    create_algorithm_selection_section(options_frame)
    create_start_button(root)

def create_who_starts_section(options_frame):
    #THE FIRST SECTION IS FOR CHOSING WHO STARTS THE GAME 
    who_starts_label = ttk.Label(options_frame, text="⭐Choose who starts the game:", foreground="dark blue", font=("Comic Sans MS", 12))
    who_starts_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    who_starts_var = tk.StringVar(root)
    who_starts_var.set("User")  # User is default selection
    user_radio = ttk.Radiobutton(options_frame, text="👤User", variable=who_starts_var, value="User", style="Custom.TRadiobutton")
    user_radio.grid(row=0, column=1, padx=5, pady=5)

    computer_radio = ttk.Radiobutton(options_frame, text="🤖Computer", variable=who_starts_var, value="Computer", style="Custom.TRadiobutton")
    computer_radio.grid(row=0, column=2, padx=5, pady=5)
    default_starter = who_starts_var.get()
    

    
def create_algorithm_selection_section(options_frame):
    #THE SECOND SECTION IS FOR CHOSING THE ALGORITHM
    algorithm_label = ttk.Label(options_frame, text="🃏Choose an algorithm: ", foreground="dark blue", font=("Comic Sans MS", 12))
    algorithm_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    algorithm_options = ["Minimax", "Alpha-Beta"]
    algo_var = tk.StringVar(root)
    algo_var.set(algorithm_options[0])
    algorithm_dropdown = ttk.Combobox(options_frame, textvariable=algo_var, values=algorithm_options, state="readonly")
    algorithm_dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
    choosen_algo = algo_var.get()
   
def create_start_button(root):
    start_button = ttk.Button(root, text="Start Game", image=start_icon, compound=tk.LEFT, command=lambda: start_game(original_number) if original_number != "0" else None, style="Custom.TButton", width=15)
    start_button.grid(row=2, column=0, pady=10, padx=(260, 180), sticky="w")

def create_game_board(root):
    game_board_frame = ttk.Frame(root)
    game_board_frame.grid(row=3, column=0, pady=10, padx=(245, 180), sticky="w")
  
    create_game_board_labels(game_board_frame)

def create_game_board_labels(game_board_frame):
    if actual_state is not None:
        labels_info = [
        ("💯Current Number: " + str(actual_state.actual_number), 0),
        ("👑User Points: " + str(actual_state.points_player1), 1),
        ("🤖Computer Points: " + str(actual_state.points_player2), 2),
        ("💰Bank Points: " + str(actual_state.bank), 3)
        ]
    else:
        labels_info = [
        ("💯Current Number: ", 0),
        ("👑User Points: ", 1),
        ("🤖Computer Points: ", 2),
        ("💰Bank Points: ", 3)
        ]
    for label_text, row in labels_info:
        label = ttk.Label(game_board_frame, text=label_text, foreground="dark blue", font=("Comic Sans MS", 12))
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
   
def create_divider_selection(root):
    global original_number, selected_number, selected_number_str
    numbers_label = ttk.Label(root, text="🧩Select a number among generated numbers to start the game with🎯", foreground="dark blue", font=("Comic Sans MS", 12))
    numbers_label.grid(row=4, column=0, padx=60, pady=5, sticky="ew")

    divisible_numbers = generate_numbers()
    numbers_var = tk.StringVar(root)
    numbers_dropdown = ttk.Combobox(root, textvariable=numbers_var, values=divisible_numbers, state="readonly")
    numbers_dropdown.grid(row=5, column=0, padx=200, pady=5, sticky="ew")

    def update_original_number():
        global original_number
        original_number = numbers_var.get()

    numbers_dropdown.bind("<<ComboboxSelected>>", lambda event: update_original_number())


    divider_label = ttk.Label(root, text="🎰Select a divider:", foreground="dark blue", font=("Comic Sans MS", 12))
    divider_label.grid(row=8, column=0, padx=255, pady=5, sticky="w")

    divider_var = tk.StringVar(root)
    divider_dropdown = ttk.Combobox(root, textvariable=divider_var, values=[2, 3, 4], state="readonly")
    divider_dropdown.grid(row=9, column=0, padx=255, pady=5, sticky="w")

    def update_selected_number():
        print("cest appele")
        global selected_number
        selected_number_str = divider_var.get()
        if selected_number_str != "":
            print("ouais pas mal")
            selected_number = int(selected_number_str)

    divider_dropdown.bind("<<ComboboxSelected>>", lambda event: update_selected_number())



    #divider_dropdown.bind("<<ComboboxSelected>>", lambda event: update_selected_number())

    current_number_var = tk.StringVar(root)
    current_number_var.set("")  # Initially empty
    current_number_display = ttk.Label(root, textvariable=current_number_var, foreground="dark blue", font=("Comic Sans MS", 12))
    current_number_display.grid(row=11, column=1, padx=5, pady=5, sticky="w")

    # when the divider (2,3,4) is selected by the user show the divide_number 
    divider_dropdown.bind("<<ComboboxSelected>>", lambda event: divide_number(divider_var, numbers_dropdown, current_number_var))
    create_move_and_new_game_buttons(root)



def create_move_and_new_game_buttons(root):
    move_button = ttk.Button(root, text="Make Move", image=move_icon, compound=tk.LEFT, command=lambda: make_move(selected_number) if selected_number != 0 else None, style="Custom.TButton")
    #move_button = ttk.Button(root, text="Make Move", image=move_icon, compound=tk.LEFT, command=lambda divider=selected_number: make_move(divider) if selected_number != 0 else None, style="Custom.TButton")

    move_button.grid(row=10, column=0, pady=10, padx=(270, 180), sticky="w")

    new_game_button = ttk.Button(root, text="Start New Game", image=new_game_icon, compound=tk.LEFT, command=start_new_game, style="Custom.TButton")
    new_game_button.grid(row=11, column=0, pady=10, padx=(260, 180),  sticky="w")

def divide_number(divider_var, numbers_dropdown, current_number_var):
    selected_divider = int(divider_var.get())
    current_number_str = numbers_dropdown.get()
    if current_number_str:
        current_number = int(current_number_str)
        result = current_number // selected_divider
        current_number_var.set(result)


title_icon = tk.PhotoImage(file="static.png")
move_icon = tk.PhotoImage(file="algorithm.png")
start_icon=tk.PhotoImage(file="start.png")
new_game_icon =tk.PhotoImage(file="rocket.png")


create_gui(root)
