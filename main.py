# Import Part

from tkinter import *
import random

# Global variables


SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#39ff14'
FOOD_COLOR = '#ffd700'
BACKGROUND_COLOR = '#4e1609'
LEVEL_SPEED = {'Easy': 130, 'Medium': 95 , 'Hard': 70}
LEVEL_POINTS = {'Easy': 1, 'Medium': 3, 'Hard': 5}


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)






class Food:
    def __init__(self):
        self.generate_food()

    def generate_food(self):
        while True:
            x = random.randint(0, (canvas.winfo_width() // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (canvas.winfo_height() // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates = [x, y]
            self.points = LEVEL_POINTS[current_level]

            if not self.is_food_on_snake():
                canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag = 'food')
                break

    def is_food_on_snake(self):
        return self.coordinates in snake.coordinates







def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += food.points
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food.generate_food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)




def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction




def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= canvas.winfo_width() or y < 0 or y >= canvas.winfo_height():
        return True
    return any(x == bx and y == by for bx, by in snake.coordinates[1:])






def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50, font=('consolas', 70), 
                       text='Game Over', fill='red', tag='gameover')
    window.after(2000, start_screen)



def reset_game():
    global score, snake, food, direction, current_level
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    countdown(5)





def select_level(level):
    global SPEED, current_level
    SPEED = LEVEL_SPEED[level]
    current_level = level
    canvas.delete("level")
    canvas.delete("level_buttons")
    canvas.create_text(canvas.winfo_width() / 2 , canvas.winfo_height() / 2 - 50, text = f"LEVEL: {level}", font=('consolas', 40), fill='white')
    window.after(1000, start_game)




def display_level_selection():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 100, text="Select Level", font = ('cosnolas', 40), fill='white', tag='level')
    levels = ['Easy', 'Medium', 'Hard']

    for i, level in enumerate(levels):
        button = Button(window, text=level, command = lambda l = level:select_level(l), font = ('consolas', 20))
        canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height()/ 2 + i * 50, window=button, tags='level_buttons')





def countdown(count):
    if count > 0:
        canvas.delete("countdown")
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 20),
                           text=str(count), fill='white', tag='countdown')
        window.after(1000, countdown, count - 1)
    else:
        canvas.delete("countdown")
        next_turn(snake, food)




def start_game():
    canvas.delete(ALL)
    reset_game()




def start_screen():
    canvas.delete(ALL)

    # Buton joc nou

    new_game_button = Button(window, text = "New Game", command = start_game, font = ("consolas", 20))
    new_game_button.pack(pady=10)
    canvas.create_window(canvas.winfo_width() / 2 , canvas.winfo_height() / 2, window= new_game_button)

    #Buton pentru select level

    select_level_button = Button(window, text = "Select Dificulty", command = display_level_selection, font = ("consolas", 20))
    select_level_button.pack(pady=10)
    canvas.create_window(canvas.winfo_width() / 2 , canvas.winfo_height() / 2 + 70, window = select_level_button)


    #Button pentru exit

    exit_button = Button(window, text = "Exit", command = window.quit, font = ("consolas", 20))
    exit_button.pack(pady=10)
    canvas.create_window(canvas.winfo_width()/ 2, canvas.winfo_height() / 2 + 140, window = exit_button)


window = Tk()
window.title("Snake game")
window.attributes('-fullscreen', True)



score = 0
direction = 'down'
current_level = 'Medium'
SPEED = LEVEL_SPEED[current_level]



label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()



canvas = Canvas(window, bg=BACKGROUND_COLOR, height=window.winfo_screenheight(), width=window.winfo_screenwidth())
canvas.pack()

window.update()
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))




start_screen()
window.mainloop()
