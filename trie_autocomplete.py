from tkinter import *

class AutocompleteEntryTrie(Entry):
    def __init__(self, trie, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.trie = trie
        self.var = StringVar()
        self["textvariable"] = self.var
        self.var.trace('w', self.update_autocomplete_list)
        self.autocompleteWindow = None
        self.lb = None

        self.config(font=('Arial', 12))

    def update_autocomplete_list(self, *args):
        if self.autocompleteWindow or self.lb:
            self.autocompleteWindow.destroy()
            self.autocompleteWindow = None
            self.lb = None

        text = self.var.get()


        if text == '':
            return

        matches = self.trie.search(text)

        if len(matches) == 0:
            return

        if len(matches) > 5:
            matches = matches[:5]

        self.autocompleteWindow = Toplevel(self)
        self.autocompleteWindow.overrideredirect(True)
        self.autocompleteWindow.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty() + self.winfo_height()}')

        height = min(5, len(matches))

        self.lb = Listbox(self.autocompleteWindow, height=height,
                          font=('Arial', 12))  # Adjust the font family and size as desired
        self.lb.pack()

        for item in matches:
            self.lb.insert("end", item)

        self.lb.bind("<Double-Button-1>", self.selection)
        self.lb.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.lb.selection_set(0)

    def selection(self, event):
        if self.lb:
            self.var.set(self.lb.get(ACTIVE))
            self.autocompleteWindow.destroy()
            self.autocompleteWindow = None
            self.lb = None

    def move_up(self, event):
        if self.lb:
            current_selection = self.lb.curselection()
            if current_selection == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def move_down(self, event):
        if self.lb:
            current_selection = self.lb.curselection()
            if current_selection == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)
