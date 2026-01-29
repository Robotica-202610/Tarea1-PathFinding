import tkinter as tk

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple GUI")

        self.label = tk.Label(master, text="Hello, World!")
        self.label.pack()

        self.greet_button = tk.Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

    def greet(self):
        self.label.config(text="Greetings from the GUI!")


def start_gui():
    """
    Starts the graphical user interface (GUI) for the application.
    Returns: None
    """
    root = tk.Tk()
    gui = SimpleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()