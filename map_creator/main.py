import os
import os.path
import tkinter

from ..common import Type

from .canvas import Canvas
from .data import Data
from .popup import Popup

class Window(tkinter.Tk):
    def __init__(self, name="Untitled", width=30, height=30, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(name)
        data = Data(name=name, width=width, height=height)
        self.set_data(data)

        self.menu = self.create_menu()
        self.config(menu=self.menu)

        self.set_unsaved_changes(False)

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
        file_menu.add_command(label="Rename", underline=0, command=self.save_as, accelerator="Ctrl+Shift+R")
        self.bind_all("<Control-Shift-r>", self.rename)
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

        tool_menu.robot_menu = self.create_robot_menu()
        tool_menu.add_cascade(label="Robot", menu=tool_menu.robot_menu, underline=0)

        return tool_menu

    def create_robot_menu(self, root):
        robot_menu = tkinter.Menu(root, tearoff=0)

        robots = [type.name for type in Type.ALL_TYPES]
        robot_menu.robot = tkinter.StringVar(robot_menu, robots[0])
        for robot in robots:
            robot_menu.add_radiobutton(label=robot, underline=0, variable=robot_menu.robot)

        return robot_menu

    def set_data(self, data):
        self.data = data
        self.set_unsaved_changes(False)
        self.canvas.destroy()
        self.canvas = Canvas(self, data)
        self.canvas.pack()

    def set_unsaved_changes(self, value):
        self.unsaved_changes = value
        if self.unsaved_changes:
            self.title("*" + self.data.name + "*")
        else:
            self.title(self.data.name)

    def check_unsaved_changes(self, title="Continue",
            message="You still have unsaved changes. Are you sure you want to continue?"):
        """
        Checks with the user if they want to do an action even though they have
        unsaved changes.
        """
        if not self.unsaved_changes:
            return True
        else:
            return messagebox.askokcancel(title, message)

    def new(self):
        """
        Create a new map
        """
        if not self.check_unsaved_changes("New"):
            return

        def action(name="Untitled", width=30, height=30):
            self.title(name)
            data = Data(name=self.name, width=width, height=height)
            self.set_data(data)

        popup = Popup({"name": "str", "width": "int", "height": "int"}, action, title="New Map")
        popup.mainloop()

    def open(self):
        """
        Open a saved map
        """

        if not self.check_unsaved_changes("Open"):
            return

        initial_directory = self.data.save_location if self.data.save_location else os.getcwd()
        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]

        file = filedialog.askopenfile(initialdir=initial_directory,
            filetypes=mask, mode="r")
        if file is None:
            return
        data = Data(file=file.name)
        file.close()

        self.set_data(data)
        self.set_unsaved_changes(False)

    def save(self, event=None):
        """
        Save our map, asking for a save location if one is not yet chosen
        """
        if self.data.save_location is None:
            self.save_as()
            return

        data.save()
        self.set_unsaved_changes(False)

    def save_as(self, event=None):
        """
        Save our map as a different file
        """
        initial_directory = self.data.save_location if self.data.save_location else os.getcwd()
        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.asksaveasfile(initialdir=initial_directory,
            initialfile=self.name, filetypes=mask, defaultextension=".wcm",
            mode="w")
        if file is None:
            return
        self.data.set_save_location(file.name)
        file.close()

        self.data.save()
        self.set_unsaved_changes(False)

    def quit(self, event=None):
        """
        Actions to be taken upon quiting
        """
        if self.check_unsaved("Quit"):
            self.destroy()


def main():
    window = Window()
    window.mainloop()

if __name__ == "__main__":
    main()
