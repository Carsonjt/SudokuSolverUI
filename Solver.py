from tkinter import *
from tkinter import messagebox
import time

#initialize and configure window
window = Tk()
window.title("Sudoku Solver")
window.resizable(False,False)
window.geometry("328x410")
labels = [0,0,0,0,0,0,0,0,0]
complete = False

#initialize 2d labels array for board
for i in range(9):
    labels[i] = [0,0,0,0,0,0,0,0,0]


complete = False

#find all valid options for row r, column c on board b
def findValids(b, r, c):
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # check rows
    for row in b[r]:
        if row in list:
            list.remove(row)
    # check columns
    for col in b:
        if col[c] in list:
            list.remove(col[c])
    # check grids
    c_grid = c // 3
    r_grid = r // 3
    for row in range((r_grid * 3), (r_grid * 3) + 3):
        for col in range((c_grid * 3), (c_grid * 3) + 3):
            if b[row][col] in list:
                list.remove(b[row][col])
    return list

#find next empty spot in board to solve (returns -1 if none AKA completed)
def findNextEmpty(b):
    for r in range(9):
        for c in range(9):
            if b[r][c] == 0:
                return r, c
    return -1

#recursive backtracking solver
def solve(b):
    global complete

    #if completed, stop (faster execution)
    if complete:
        return

    #if board is completed, input solution to UI and set to completed
    if findNextEmpty(b) == -1:
        for x in range(9):
            for y in range(9):
                labels[x][y].configure(text=str(b[x][y]))

        complete = True
        return

    #not completed -> find next location and begin attempting all valid numbers for that location, revert back if none are successful
    r, c = findNextEmpty(b)
    valids = findValids(b, r, c)
    for num in valids:
        b[r][c] = num
        solve(b)
    b[r][c] = 0


#convert 2d labels grid to int board grid for easier use
def labelsToBoard():
    #start as empty board
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    #add any values to empty board
    for x in range(9):
        for y in range(9):
            if labels[x][y].cget("text") != " ":
                board[x][y] = int(labels[x][y].cget("text"))
            else:
                labels[x][y].configure(fg="gray")
               
    #return updated board
    return board


#Ensure that entired board is valid before attempting to solve and highlight errors
def initallyValid():
    #check each input value
    for x in range(9):
        for y in range(9):
            if labels[x][y].cget("text") != " ":
                #check row
                for row in labels[x]:
                    if row.cget("text") == labels[x][y].cget("text") and row != labels[x][y]:
                        row.configure(bg="red")
                        labels[x][y].configure(bg="red")
                        return False
                #check col
                for col in labels:
                    if col[y].cget("text") == labels[x][y].cget("text") and col[y] != labels[x][y]:
                        col[y].configure(bg="red")
                        labels[x][y].configure(bg="red")
                        return False
                #check grid
                c_grid = y // 3
                r_grid = x // 3
                for row in range((r_grid * 3), (r_grid * 3) + 3):
                    for col in range((c_grid * 3), (c_grid * 3) + 3):
                        if labels[row][col].cget("text") == labels[x][y].cget("text") and labels[row][col] != labels[x][y]:
                            labels[row][col].configure(bg="red")
                            labels[x][y].configure(bg="red")
                            return False
    return True


#######################################
#                                     #
#   BUTTON/LABEL EVENTS FOR TKINTER   #
#                                     #
#######################################

#Runs when "Click to Solve Solve" is clicked
def attemptSolve():
    if initallyValid():
        solve(labelsToBoard())
        if not complete:
            messagebox.showerror("Error", "Invalid Sudoku. No solution found")
    else:
        messagebox.showerror("Error", "Invalid Sudoku. Conflicts found")


#Runs when "ResetBoard" is clicked
def clearBoard():
    for x in range(9):
        for y in range(9):
            labels[x][y].configure(text=" ", fg="black")
    global complete
    complete = False

#Runs when board is right-clicked
def rightClick(event):
    if complete:
        return

    for x in range(9):
        for y in range(9):
            labels[x][y].configure(bg="#d3d3d3")

    next = event.widget.cget("text")
    if next == " ":
        next = "9"
    elif next == "1":
        next = " "
    else:
        next = str(int(next) - 1)
    event.widget.configure(text=next)

#Runs when board is left-clicked
def leftClick(event):
    if complete:
        return

    for x in range(9):
        for y in range(9):
            labels[x][y].configure(bg="#d3d3d3")

    next = event.widget.cget("text")
    if next == " ":
        next = "1"
    elif next == "9":
        next = " "
    else:
        next = str(int(next) + 1)
    event.widget.configure(text=next)

#######################################
#                                     #
#    BUTTON/LABEL SETUP FOR TKINTER   #
#                                     #
#######################################

#Create grid of labels 
for x in range(9):
    for y in range(9):
        labels[x][y] = Label(text=" ", width=2,height=0,bg="#d3d3d3",font=('Cambria', 19))

        labels[x][y].bind("<Button-1>", leftClick)
        labels[x][y].bind("<Button-2>", rightClick)
        labels[x][y].bind("<Button-3>", rightClick)
        if x % 3 == 2 and y % 3 == 2 and x != 8 and y != 8:
            labels[x][y].grid(row=x, column=y, padx=(1, 3), pady=(1, 3))
        elif x % 3 == 2 and x != 8:
            labels[x][y].grid(row=x, column=y, pady=(1,3))
        elif y % 3 == 2 and y != 8:
            labels[x][y].grid(row=x, column=y, padx=(1, 3))
        else:
            labels[x][y].grid(row=x, column=y, padx=1, pady=1)

#create clear and solve buttons
clear_button = Button(text="Reset Board",font=('Impact', 19), bg="#d3d3d3", borderwidth=2, relief="solid", command=clearBoard)
clear_button.place(x=5,y=350)
solve_button = Button(text="Click to Solve", font=('Impact', 19), bg="#d3d3d3", borderwidth=2, relief="solid", command=attemptSolve)
solve_button.place(x=168,y=350)

#create bars between grids
hor_bar = Frame(master=window, width=328,height=4, bg="black")
hor_bar2 = Frame(master=window, width=328,height=4, bg="black")
vert_bar = Frame(master=window, width=4,height=346, bg="black")
vert_bar2 = Frame(master=window, width=4,height=346, bg="black")
hor_bar.place(x=0, y=113)
hor_bar2.place(x=0, y=229)
vert_bar.place(x=107, y=0)
vert_bar2.place(x=217, y=0)

#open window
window.mainloop()