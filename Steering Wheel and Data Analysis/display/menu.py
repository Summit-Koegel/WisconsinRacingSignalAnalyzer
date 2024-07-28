import tkinter as tk
from tkinter import ttk

class MenuScreen:
    def __init__(self, root, screens):
        self.root = root
        self.screens = screens
        self.selected_index = 0
        
        self.screen_names = ["E-Car Drive", "C-Car Drive", "Settings"]
        
        self.screen_rectangles = []
        for i, name in enumerate(self.screen_names):
            rectangle = ttk.Label(root, text=name, font=("Arial", 20))
            rectangle.grid(row=i, padx=10, pady=10, sticky="w")
            self.screen_rectangles.append(rectangle)
        
        self.highlight_screen()

    def highlight_screen(self):
        for i, rectangle in enumerate(self.screen_rectangles):
            if i == self.selected_index:
                rectangle.configure(background="blue")
            else:
                rectangle.configure(background="gray")

    def on_joystick_up_pressed(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.highlight_screen()

    def on_joystick_down_pressed(self):
        if self.selected_index < len(self.screen_names) - 1:
            self.selected_index += 1
            self.highlight_screen()

    def on_joystick_center_pressed(self):
        selected_screen = self.screen_names[self.selected_index]
        if selected_screen in self.screens:
            self.screens[selected_screen].pack()
            self.root.title(selected_screen)

class DriveDisplay:
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.label = ttk.Label(root, text=name, font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Steering Wheel")

    screens = {}
    screens["E-Car Drive"] = DriveDisplay(root, "E-Car Drive Screen")
    screens["C-Car Drive"] = DriveDisplay(root, "C-Car Drive Screen")
    screens["Settings"] = DriveDisplay(root, "Settings Screen")

    menu = MenuScreen(root, screens)

    root.mainloop()
