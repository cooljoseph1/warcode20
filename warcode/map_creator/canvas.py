import os, os.path

import tkinter
from PIL import ImageTk, Image

_my_dir = os.path.dirname(os.path.realpath(__file__))
_image_dir = os.path.abspath(os.path.join(_my_dir, os.pardir, os.pardir, "resources", "images"))

class Canvas(tkinter.Canvas):
    COLORS = {
        "EMPTY": "white",
        "WALL": "black",
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

        self.images = {
            "WALL": self.load_image("wall.png"),
            "GOLD_MINE": self.load_image("gold_mine.png"),
            "TREE": self.load_image("tree.png"),
            "RED_ARCHER": self.load_image("robots/red_archer.png"),
            "RED_HORSE": self.load_image("robots/red_horse.png"),
            "RED_PEASANT": self.load_image("robots/red_peasant.png"),
            "RED_PIKE": self.load_image("robots/red_pike.png"),
            "RED_HOUSE": self.load_image("robots/red_house.png"),
            "BLUE_ARCHER": self.load_image("robots/blue_archer.png"),
            "BLUE_HORSE": self.load_image("robots/blue_horse.png"),
            "BLUE_PEASANT": self.load_image("robots/blue_peasant.png"),
            "BLUE_PIKE": self.load_image("robots/blue_pike.png"),
            "BLUE_HOUSE": self.load_image("robots/blue_house.png"),
        }

        self.square_array = [
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

        self.image_array = [
            [None for x in range(self.map_data.width)]
            for y in range(self.map_data.height)
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

    def update(self, changed_locations=None):
        if changed_locations:
            for (x, y) in changed_locations:
                self.update_loc(x, y)
            return

        for y in range(self.map_data.height):
            for x in range(self.map_data.width):
                self.update_loc(x, y)

    def update_loc(self, x, y):
        if self.image_array[y][x]:
            self.delete(self.image_array[y][x])

        square = self.map_data.map[y][x]
        if square == " ":
            return

        image = self.get_image(square)
        scaled_x, scaled_y = self.scale(x, y)
        self.image_array[y][x] = self.create_image(scaled_x, scaled_y, image=image, anchor=tkinter.NW)

    def get_image(self, square):
        if square == "W":
            return self.images["WALL"]
        if square in self.map_data.gold_mines:
            return self.images["GOLD_MINE"]
        if square in self.map_data.trees:
            return self.images["TREE"]
        robot = self.map_data.robots[square]
        type = robot.type.to_string()
        team = robot.team.to_string()
        return self.images[team + "_" + type]

    def load_image(self, name):
        file = os.path.join(_image_dir, name)
        image = Image.open(file)
        image = image.resize((int(self.square_size), int(self.square_size)), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image
