from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SudokuSolver(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuSolver, self).__init__(**kwargs)
        # Setting number of rows and columns in grid layout
        self.cols = 9
        self.rows = 10
        # Creating a 2D list of TextInputs
        self.inputs = [[TextInput(multiline=False) for j in range(self.cols)] for i in range(self.rows-1)]
        # Adding the TextInputs to the layout
        for row in self.inputs:
            for input in row:
                self.add_widget(input)
        # Creating a Solve button
        self.solve_button = Button(text="Solve")
        self.solve_button.bind(on_press=self.solve)
        self.add_widget(self.solve_button)

    def solve(self, instance):
        # Convert the input values to a 2D list of integers
        values = [[int(input.text) if input.text.isdigit() else 0 for input in row] for row in self.inputs]
        # Call the solve_recursive() function to solve the puzzle
        if self.solve_recursive(values):
            # If a solution is found, update the input values with the solution
            for i in range(self.rows-1):
                for j in range(self.cols):
                    self.inputs[i][j].text = str(values[i][j])

    def solve_recursive(self, values):
        # Find the next empty cell
        row, col = self.find_empty(values)
        # If all cells are filled, the puzzle is solved
        if row == -1:
            return True
        # Try all possible values in the empty cell
        for num in range(1, 10):
            # Check if the value is valid in the current cell
            if self.is_valid(values, row, col, num):
                # If the value is valid, set the cell to the value
                values[row][col] = num
                # Recursively call solve_recursive() to solve the puzzle
                if self.solve_recursive(values):
                    return True
                # If the recursive call fails, backtrack and try the next value
                values[row][col] = 0
        # If no value works, the puzzle is unsolvable
        return False

    def find_empty(self, values):
        # Find the next empty cell in the puzzle
        for i in range(len(values)):
            for j in range(len(values[i])):
                if values[i][j] == 0:
                    return i, j
        return -1, -1

    def is_valid(self, values, row, col, num):
        # Check if the value is valid in the current cell, row, or column
        # Check the row
        for i in range(len(values[row])):
            if values[row][i] == num:
                return False
        # Check the column
        for i in range(len(values)):
            if values[i][col] == num:
                return False
        # Check the 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row+3):
            for j in range(box_col, box_col+3):
                if values[i][j] == num:
                    return False
        return True

class SudokuApp(App):
    def build(self):
       return SudokuSolver()

if __name__ == 'main':
    SudokuApp().run()