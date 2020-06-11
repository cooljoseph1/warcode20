import tkinter
from ..common import Type, Team

from .canvas import Canvas
from .map_data import MapData
from .popup import Popup

class Window(tkinter.Tk):
    def __init__(self, *args, save_file=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_data = MapData(save_file=save_file)
        self.canvas = Canvas(self, self.map_data)

        self.menu = self.create_menu()
        self.config(menu=self.menu)

        self.set_saved()

    def create_menu(self):
        menu = tkinter.Menu(self)

        menu.file_menu = self.create_file_menu(menu)
        menu.symmetry_menu = self.create_symmetry_menu(menu)
        menu.tool_menu = self.create_tool_menu(menu)

        menu.add_cascade(label="File", menu=menu.file_menu, underline=0)
        menu.add_cascade(label="Symmetry", menu=menu.symmetry_menu, underline=0)
        menu.add_cascade(label="Tool", menu=menu.tool_menu, underline=0)

        return menu

    def create_file_menu(self, root):
        file_menu = tkinter.Menu(root, tearoff=0)

        file_menu.add_command(label="New", underline=0, command=self.new, accelerator="Ctrl+N")
        self.bind_all("<Control-n>", self.new)
        file_menu.add_command(label="Open", underline=0, command=self.open, accelerator="Ctrl+O")
        self.bind_all("<Control-o>", self.open)
        file_menu.add_command(label="Save", underline=0, command=self.save, accelerator="Ctrl+S")
        self.bind_all("<Control-s>", self.save)
        file_menu.add_command(label="Save As", underline=5, command=self.save_as, accelerator="Ctrl+Shift+S")
        self.bind_all("<Control-Shift-s>", self.save_as)
        file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator="Ctrl+Shift+Q")
        self.bind_all("<Control-Shift-q>", self.quit)

        return file_menu

    def create_symmetry_menu(self, root):
        symmetry_menu = tkinter.Menu(root, tearoff=0)

        symmetries = ["None", "Horizontal", "Vertical", "UR Diagonal", "DR Diagonal", "Radial"]
        symmetry_menu.symmetry = tkinter.StringVar(symmetry_menu, symmetries[1])
        for symmetry in symmetries:
            symmetry_menu.add_radiobutton(label=symmetry, underline=0, variable=symmetry_menu.symmetry)

        return symmetry_menu

    def create_tool_menu(self, root):
        tool_menu = tkinter.Menu(root, tearoff=0)

        tools = ["Empty", "Wall", "Gold Mine", "Tree"]
        tool_menu.tool = tkinter.StringVar(tool_menu, tools[1])
        for tool in tools:
            tool_menu.add_radiobutton(label=tool, underline=0, variable=tool_menu.tool)

        tool_menu.robot_menu = self.create_robot_menu(tool_menu)
        tool_menu.add_cascade(label="Robot", menu=tool_menu.robot_menu, underline=0)

        return tool_menu

    def create_robot_menu(self, root):
        robot_menu = tkinter.Menu(root, tearoff=0)

        robots = [type.name.title() for type in Type.ALL_TYPES]
        for robot in robots:
            robot_menu.add_radiobutton(label=robot, underline=0, variable=root.tool)

        return robot_menu

    def set_unsaved(self):
        self.unsaved_changes = True
        self.title("*" + self.map_data.name + "*")

    def set_saved(self):
        self.unsaved_changes = False
        self.title(self.map_data.name)

    def check_unsaved(self, title="Continue",
            message="You still have unsaved changes. Are you sure you want to continue?"):
        """
        Checks with the user if they want to do an action even though they have
        unsaved changes.
        """
        if not self.unsaved_changes:
            return True
        else:
            return messagebox.askokcancel(title, message)

    def new(self, event=None):
        def process_new(name, width, height):
            self.map_data = MapData(width=width, height=height, name=name)
            self.canvas.destroy()
            self.canvas = Canvas(self, self.map_data)
            self.set_saved()

        popup = Popup(
            {"name": str, "width": int, "height": int},
            process_new,
            "New",
        )

    def open(self, event=None):
        pass

    def save(self, event=None):
        pass

    def save_as(self, event=None):
        pass

    def quit(self, event=None):
        pass

    def set_square(self, x, y):
        tool = self.menu.tool_menu.tool.get()
        if tool == "Empty":
            self.map_data.set(x, y, " ")
        elif tool == "Wall":
            self.map_data.set(x, y, "W")
        elif tool == "Gold Mine":
            self.map_data.add_gold_mine(x, y)
        elif tool == "Tree":
            self.map_data.add_tree(x, y)
        else:
            self.map_data.add_robot(x, y, Type.from_string(tool.upper()), Team.RED)
        self.canvas.update()
