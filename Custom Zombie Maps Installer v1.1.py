import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess
import shutil
import webbrowser

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Custom Zombie Maps Installer - Black Ops III.")
        self.geometry("400x350")

        self.create_widgets()

    def create_widgets(self):
        self.workshop_button = tk.Button(self, text="Open the Steam Workshop website", command=self.open_workshop)
        self.workshop_button.pack(pady=10)

        self.game_directory_button = tk.Button(self, text="Select the game directory", command=self.set_game_directory)
        self.game_directory_button.pack(pady=10)

        self.game_directory_label = tk.Label(self, text="")
        self.game_directory_label.pack(pady=5)
        self.update_game_directory_label()

        self.workshop_id_label = tk.Label(self, text="Enter the Workshop ID of the item:")
        self.workshop_id_label.pack(pady=10)

        self.workshop_id_entry = tk.Entry(self)
        self.workshop_id_entry.pack()

        self.download_button = tk.Button(self, text="Download and install", command=self.start_download)
        self.download_button.pack(pady=10)
        
        self.game_directory_label = tk.Label(self, text="If the application is unresponsive, it is downloading the item.")
        self.game_directory_label.pack(pady=5)
        
        self.game_directory_label = tk.Label(self, text="Please check the Python console to track the progress.")
        self.game_directory_label.pack(pady=5)

        self.quit_button = tk.Button(self, text="Exit", command=self.quit)
        self.quit_button.pack(pady=5)
        
        self.add_credits()

    def open_workshop(self):
        workshop_url = "https://steamcommunity.com/workshop/browse/?appid=311210&requiredtags[]=Zombies"
        webbrowser.open(workshop_url)

    def set_game_directory(self):
        game_directory = filedialog.askdirectory(title="Select the game directory for Call of Duty Black Ops III")
        if game_directory:
            with open("game_directory.txt", "w") as file:
                file.write(game_directory)
                messagebox.showinfo("Success", "The game directory has been saved.")
            self.update_game_directory_label()

    def update_game_directory_label(self):
        if os.path.exists("game_directory.txt"):
            with open("game_directory.txt", "r") as file:
                directory = file.read().strip()
            self.game_directory_label.configure(text=f"Game directory : {directory}")
        else:
            self.game_directory_label.configure(text="Game directory not set")

    def get_game_directory(self):
        if os.path.exists("game_directory.txt"):
            with open("game_directory.txt", "r") as file:
                directory = file.read().strip()
            return directory
        else:
            messagebox.showerror("Error", "The game directory has not been set.")
            return None

    def download_workshop_item(self, workshop_id):
        try:
            subprocess.check_call(["steamcmd", "+login", "anonymous", "+workshop_download_item", "311210", workshop_id, "+quit"])
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "The download has failed. Please try again.")

    def get_folder_name(self, workshop_id):
        workshop_path = os.path.join("steamapps", "workshop", "content", "311210", workshop_id, "workshop.json")
        with open(workshop_path, "r") as file:
            data = json.load(file)
            folder_name = data["FolderName"]
        return folder_name

    def install_files(self, workshop_id, folder_name, game_directory):
        source_folder = os.path.join("steamapps", "workshop", "content", "311210", workshop_id)
        destination_folder = os.path.join(game_directory, "usermaps", folder_name)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_folder)
                dest_path = os.path.join(destination_folder, rel_path)

                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                shutil.copy2(src_path, dest_path)

    def start_download(self):
        workshop_id = self.workshop_id_entry.get()
        game_directory = self.get_game_directory()

        if game_directory is not None:
            self.download_workshop_item(workshop_id)
            folder_name = self.get_folder_name(workshop_id)
            self.install_files(workshop_id, folder_name, game_directory)

            messagebox.showinfo("Success", "The installation is complete.")
            view_folder = messagebox.askyesno("View the folder", "Do you want to open the created folder?")
            if view_folder:
                os.startfile(os.path.join(game_directory, "usermaps", folder_name))
                
    def add_credits(self):
        credits_text = "Created by Alexandre Hemery - "
        github_text = "Github"
        
        self.credits_text_widget = tk.Text(self, height=2, wrap=tk.WORD, padx=3, pady=3, relief=tk.FLAT, bg=self.cget('bg'), cursor="arrow")
        
        self.credits_text_widget.tag_configure("credits_text", font=("TkDefaultFont", 8))
        self.credits_text_widget.tag_configure("github_link", foreground="blue", underline=True, font=("TkDefaultFont", 8))
        self.credits_text_widget.tag_bind("github_link", "<Button-1>", self.open_github)
        
        self.credits_text_widget.insert(tk.INSERT, credits_text, ("credits_text",))
        self.credits_text_widget.insert(tk.INSERT, github_text, ("github_link",))
        
        self.credits_text_widget.config(state=tk.DISABLED)
        self.credits_text_widget.pack(side=tk.BOTTOM, anchor="sw")
        
    def open_github(self, event):
        webbrowser.open("https://github.com/alexandre-hemery/bo3-cm-maps-installer")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()