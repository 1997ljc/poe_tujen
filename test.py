import tkinter as tk
from pynput import keyboard

class GridCanvas(tk.Canvas):
    def __init__(self, master, rows, cols, cell_size, border_width=1, **kwargs):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.border_width = border_width
        self.grid = [[0] * cols for _ in range(rows)]  # 0 表示灰色，1 表示红色
        self.rects = {}

        width = cols * cell_size
        height = rows * cell_size
        super().__init__(master, width=width, height=height, **kwargs)

        self.bind("<Button-1>", self.on_click)

        self.draw_grid()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                rect_id = self.create_rectangle(x0, y0, x1, y1, fill="gray", outline="black", width=self.border_width)
                self.rects[(row, col)] = rect_id

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            rect_id = self.rects[(row, col)]
            if self.grid[row][col] == 0:
                self.itemconfig(rect_id, fill="red")
                self.grid[row][col] = 1
            else:
                self.itemconfig(rect_id, fill="gray")
                self.grid[row][col] = 0


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Clicker")
        self.geometry("600x400")

        self.rows, self.cols = 5, 12
        self.cell_size = 30

        self.grid_canvas = GridCanvas(self, self.rows, self.cols, self.cell_size)
        self.grid_canvas.pack()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                red_cells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.grid_canvas.grid[row][col] == 1]
                print("红色格子的位置：", red_cells)
        except AttributeError:
            pass


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()