import tkinter
from tkinter import filedialog, messagebox
import os, os.path

from ..common import Type, Team

from .canvas import Canvas
from .map_data import MapData
from .popup import Popup

_my_dir = os.path.dirname(os.path.realpath(__file__))

class Window(tkinter.Tk):
    def __init__(self, *args, save_file=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_data = MapData(save_file=save_file)
        self.canvas = Canvas(self, self.map_data)

        self.menu = self.create_menu()
        self.config(menu=self.menu)

        self.set_saved()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.resizable(False, False)

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
        file_menu.add_command(label="Rename", underline=0, command=self.rename, accelerator="Ctrl+Shift+R")
        self.bind_all("<Control-R>", self.rename)
        file_menu.add_command(label="Open", underline=0, command=self.open, accelerator="Ctrl+O")
        self.bind_all("<Control-o>", self.open)
        file_menu.add_command(label="Save", underline=0, command=self.save, accelerator="Ctrl+S")
        self.bind_all("<Control-s>", self.save)
        file_menu.add_command(label="Save As", underline=5, command=self.save_as, accelerator="Ctrl+Shift+S")
        self.bind_all("<Control-S>", self.save_as)
        file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator="Ctrl+Shift+Q")
        self.bind_all("<Control-Q>", self.quit)

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
            return messagebox.askyesno(title, message)

    def new(self, event=None):
        """
        Create a new warcode map
        """
        if not self.check_unsaved("New"):
            return

        def process_new(name, width, height):
            self.map_data = MapData(width=width, height=height, name=name)
            self.canvas.destroy()
            self.canvas = Canvas(self, self.map_data)
            self.canvas.pack()
            self.set_saved()

        popup = Popup(
            {"name": str, "width": int, "height": int},
            process_new,
            "New",
        )

    def rename(self, event=None):
        """
        Rename the map
        """
        def process_rename(name):
            self.map_data.name = name
            if self.unsaved_changes:
                self.title("*" + name + "*")
            else:
                self.title(name)

        popup = Popup(
            {"name": str},
            process_rename,
            "Rename",
        )

    def open(self, event=None):
        """
        Open a saved warcode map
        """
        if not self.check_unsaved("Open"):
            return

        if self.map_data.save_file:
            initial_directory = os.path.dirname(self.map_data.save_file)
        else:
            initial_directory = os.path.abspath(os.path.join(_my_dir, os.pardir, os.pardir, "resources", "maps"))

        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.askopenfile(
            initialdir=initial_directory,
            filetypes=mask,
            mode="r",
        )
        if file is None:
            return

        self.map_data.load(file.name)

        self.canvas.destroy()
        self.canvas = Canvas(self, self.map_data)
        self.canvas.pack()

        self.set_saved()

    def save(self, event=None):
        """
        Save our file
        """
        if self.map_data.save_file:
            self.map_data.save()
            self.set_saved()
            return

        self.save_as()

    def save_as(self, event=None):
        """
        Save our map as a different file
        """
        if self.map_data.save_file:
            initial_directory = os.path.dirname(self.map_data.save_file)
        else:
            initial_directory = os.path.abspath(os.path.join(_my_dir, os.pardir, os.pardir, "resources", "maps"))

        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.asksaveasfile(
            initialdir=initial_directory,
            initialfile=self.map_data.name,
            filetypes=mask,
            defaultextension=".wcm",
            mode="w",
        )

        if file is None:
            return

        self.map_data.save(file.name)
        self.set_saved()

    def quit(self, event=None):
        """
        Actions to be taken upon quiting
        """
        if self.check_unsaved("Quit"):
            self.destroy()

    def set_square(self, x, y):
        self.set_unsaved()
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
