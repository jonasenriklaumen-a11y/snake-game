"""Snake – kleines Spiel mit Tkinter (nur Standardbibliothek, läuft ohne Installation)."""
import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SPEED_MS = 120

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITES = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake")
        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#111",
            highlightthickness=0,
        )
        self.canvas.pack()

        for key in DIRECTIONS:
            root.bind(f"<{key}>", self.on_key)
        root.bind("<space>", self.on_restart)

        self.reset()
        self.tick()

    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        free_cells = {
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        } - set(self.snake)
        return random.choice(list(free_cells))

    def on_key(self, event):
        new_dir = event.keysym
        if OPPOSITES[new_dir] != self.direction:
            self.next_direction = new_dir

    def on_restart(self, event):
        if self.game_over:
            self.reset()

    def tick(self):
        if not self.game_over:
            self.direction = self.next_direction
            self.move_snake()
        self.draw()
        self.root.after(SPEED_MS, self.tick)

    def move_snake(self):
        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
        hit_self = new_head in self.snake
        if hit_wall or hit_self:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL_SIZE, fy * CELL_SIZE,
            fx * CELL_SIZE + CELL_SIZE, fy * CELL_SIZE + CELL_SIZE,
            fill="#e74c3c", outline="",
        )

        for i, (x, y) in enumerate(self.snake):
            color = "#2ecc71" if i == 0 else "#27ae60"
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE,
                fill=color, outline="#111",
            )

        self.canvas.create_text(
            8, 8, anchor="nw", fill="white",
            font=("Consolas", 12, "bold"),
            text=f"Punkte: {self.score}",
        )

        if self.game_over:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2,
                fill="white", font=("Consolas", 20, "bold"),
                text="Game Over\nLeertaste = neu starten",
                justify="center",
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    SnakeGame(root)
    root.mainloop()
