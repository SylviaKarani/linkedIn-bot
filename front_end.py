import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from main import LinkedInBot  

class LinkedInBotGUI:
    def __init__(self, master):
        self.master = master
        
        self.master.title("LinkedIn Bot GUI")
        
        # Initialize the Tkinter window and set up the UI components
        self.root = tk.Tk()

        self.create_widgets()
        
    def run(self):
        # Run the Tkinter main loop
        self.root.mainloop()

    def create_widgets(self):
        self.label_email = ttk.Label(self.master, text="Email:")
        self.label_email.grid(row=0, column=0, padx=5, pady=5)

        self.entry_email = ttk.Entry(self.master)
        self.entry_email.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = ttk.Label(self.master, text="Password:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)

        self.entry_password = ttk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.label_positions = ttk.Label(self.master, text="Positions (comma-separated):")
        self.label_positions.grid(row=2, column=0, padx=5, pady=5)

        self.entry_positions = ttk.Entry(self.master)
        self.entry_positions.grid(row=2, column=1, padx=5, pady=5)

        self.label_locations = ttk.Label(self.master, text="Locations (comma-separated):")
        self.label_locations.grid(row=3, column=0, padx=5, pady=5)

        self.entry_locations = ttk.Entry(self.master)
        self.entry_locations.grid(row=3, column=1, padx=5, pady=5)
        
        self.chk_easy_apply = ttk.Checkbutton(self.master, text="Easy Apply", variable=tk.BooleanVar())
        self.chk_easy_apply.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.btn_run_bot = ttk.Button(self.master, text="Run LinkedIn Bot", command=self.run_bot)
        self.btn_run_bot.grid(row=4, column=0, columnspan=2, pady=10)

    def run_bot(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        positions = [pos.strip() for pos in self.entry_positions.get().split(",")]
        locations = [loc.strip() for loc in self.entry_locations.get().split(",")]

        parameters = {
            'email': email,
            'password': password,
            'disableAntiLock': True,
            'positions': positions,
            'locations': locations,
            # Add other parameters as needed
        }

        bot = LinkedInBot(parameters)

        try:
            bot.login()
            bot.apply_filters()

        finally:
            bot.close()
            print("Script completed")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedInBotGUI()
    app.run()

