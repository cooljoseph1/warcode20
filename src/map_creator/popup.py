import tkinter
from tkinter import filedialog, ttk, messagebox

_SMALL_FONT= ("Verdana", 6)
_MEDIUM_FONT= ("Verdana", 10)
_LARGE_FONT= ("Verdana", 12)

class Popup(tkinter.Toplevel):
    def __init__(self, fields, action, title=None, *args, **kwargs):
        """
        fields:  dictionary of field name to field type
        action:  action to be called when user finishes
        title:  title of pop up box
        *args:  arguments to pass to super()
        **kwargs:  arguments to pass to super()
        """
        super().__init__(*args, **kwargs)

        self.action = action
        self.title(title)
        self.fields = {}

        self.input_frame = tkinter.Frame(self)

        for index, (field_name, field_type) in enumerate(fields.items()):
            self.fields[field_name] = Field(self.input_frame, field_name, field_type)
            self.fields[field_name].pack(index)

        self.button_frame = tkinter.Frame(self)

        cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.cancel)
        cancel_button.bind("<Return>", self.cancel)
        cancel_button.grid(row=0, column=0)

        ok_button = ttk.Button(self.button_frame, text="OK", command=self.create_new)
        ok_button.bind("<Return>", self.create_new)
        ok_button.grid(row=0, column=1)

        self.input_frame.pack(padx=20, pady=20)
        self.button_frame.pack(padx=20, pady=20, side="right")

    def cancel(self):
        self.destroy()

    def create_new(self):
        values = {name: field.get() for name, field in self.fields.items()}
        if any(val is None for val in values.values()):
            return
        self.destroy()
        self.action(**values)

class Field:
    def __init__(self, root, field_name, field_type=str, font=_MEDIUM_FONT):
        """
        root:  root popup window
        field_name:  name of the field
        field_type:  conversion to use when getting input.  E.g. int, str
        font:  override font to use
        """

        if field_type not in (str, int):
            raise ValueError("field_type must be str or int.")

        self.root = root
        self.field_name = field_name
        self.field_type = field_type

        self.label = ttk.Label(self.root, text=self.field_name.title() + ": ", font=font)
        self.entry = ttk.Entry(self.root, font=font)

    def pack(self, row):
        self.label.grid(row=row, column=0, padx=5, pady=5)
        self.entry.grid(row=row, column=1, padx=5, pady=5)

    def get(self):
        try:
            return self.field_type(self.entry.get())
        except:
            messagebox.showerror("Error", "Invalid " + self.field_name, master=self.entry)
            self.root.deiconify()
            return None
