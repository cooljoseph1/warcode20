import tkinter

class Canvas(tkinter.Canvas):
    COLORS = {
        "EMPTY": "white",
        "WALL": "black",
        "GOLD_MINE": "gold",
        "TREE": "forest green",
        "RED": "red",
        "BLUE": "blue",
    }

    def __init__(self, root, map_data, border=0, *args, **kwargs):
        """
        root -- main window
        map_data -- map data object for the map
        border -- border inside the canvas so that the rectangles are not cut off
        """

        super().__init__(root, *args, **kwargs)
        self.root = root
        self.map_data = map_data
        self.border = border

        self.square_size = self.get_optimal_square_size()
        self.width = self.square_size * self.map_data.width + 2 * self.border + 1
        self.height = self.square_size * self.map_data.height + 2 * self.border + 1
        self.config(width=self.width, height=self.height)

        self.squares = [
            [
                self.create_rectangle(
                x * self.square_size + border + 2,
                y * self.square_size + border + 2,
                (x + 1) * self.square_size + border + 2,
                (y + 1) * self.square_size + border + 2,
                outline="black",
                fill="white")
                for x in range(self.map_data.width)
            ] for y in range(self.map_data.height)
        ]

        self.bind("<Button 1>", self.mouse_click)
        self.bind("<B1 Motion>", self.mouse_click)

        self.pack()
        self.update()

    def get_optimal_square_size(self):
        return min(1600 // self.map_data.width, 800 // self.map_data.height)

    def scale(self, x, y):
        return (x * self.square_size + self.border + 2, y * self.square_size + self.border + 2)

    def scale_back(self, x, y):
        return ((x - self.border - 2) // self.square_size, (y - self.border - 2) // self.square_size)

    def mouse_click(self, event):
        x, y = self.scale_back(event.x, event.y)
        if not (0 <= x < self.map_data.width and 0 <= y < self.map_data.height):
            return # Invalid location

        self.root.set_square(x, y)

    def update(self):
        for y in range(self.map_data.height):
            for x in range(self.map_data.width):
                color = self.get_color(self.map_data.map[y][x])
                if self.itemcget(self.squares[y][x], "fill") != color:
                    self.itemconfig(self.squares[y][x], fill=color)

    def get_color(self, square):
        if square == " ":
            return Canvas.COLORS["EMPTY"]
        if square == "W":
            return Canvas.COLORS["WALL"]
        if isinstance(square, int):
            if square in self.map_data.gold_mines:
                return Canvas.COLORS["GOLD_MINE"]
            if square in self.map_data.trees:
                return Canvas.COLORS["TREE"]
            if square in self.map_data.robots:
                team = self.map_data.robots[square].team
                return Canvas.COLORS[team.to_string()]
