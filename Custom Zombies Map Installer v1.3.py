import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess
import shutil
import webbrowser
import threading

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Custom Zombies Maps Installer - Black Ops III")
        self.geometry("400x400")
        
        self.download_status_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.workshop_button = tk.Button(self, text="Open Steam Workshop website", command=self.open_workshop)
        self.workshop_button.pack(pady=10)

        self.game_directory_button = tk.Button(self, text="Select game directory", command=self.set_game_directory)
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
        
        self.download_status = tk.Label(self, textvariable=self.download_status_var)
        self.download_status.pack(pady=5)
        
        self.download_size_var = tk.StringVar()
        self.download_size = tk.Label(self, textvariable=self.download_size_var)
        self.download_size.pack(pady=5)

        self.debug_button = tk.Button(self, text="Debugging", command=self.confirm_delete)
        self.debug_button.pack(pady=5)

        self.quit_button = tk.Button(self, text="Exit", command=self.quit)
        self.quit_button.pack(pady=5)
        
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.add_credits()
        self.add_version()

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
            self.game_directory_label.configure(text=f"Game directory: {directory}")
        else:
            self.game_directory_label.configure(text="Game directory not defined")

    def get_game_directory(self):
        if os.path.exists("game_directory.txt"):
            with open("game_directory.txt", "r") as file:
                directory = file.read().strip()
            return directory
        else:
            messagebox.showerror("Error", "The game directory has not been defined.")
            return None

    def download_workshop_item(self, workshop_id):
        try:
            subprocess.check_call(["steamcmd", "+login", "anonymous", "+workshop_download_item", "311210", workshop_id, "+quit"])
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "The download has failed. Please try again.")
            
    def update_download_size(self, workshop_id):
        workshop_downloads_folder = os.path.join("steamapps", "workshop", "downloads", "311210", workshop_id)
        total_size = 0
        for root, dirs, files in os.walk(workshop_downloads_folder):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
        size_in_gb = total_size / (1024 * 1024 * 1024)
        self.download_size_var.set(f"Download size: {size_in_gb:.2f} GB")

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

        zone_folder = os.path.join(destination_folder, "zone")
        if not os.path.exists(zone_folder):
            os.makedirs(zone_folder)

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_folder)

                if "video" in root.split(os.sep):
                    dest_path = os.path.join(game_directory, "video", rel_path.replace("video" + os.sep, ""))
                else:
                    dest_path = os.path.join(zone_folder, rel_path)

                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                shutil.copy2(src_path, dest_path)

        shutil.rmtree(source_folder)

    def start_download(self):
        workshop_id = self.workshop_id_entry.get()
        game_directory = self.get_game_directory()

        if game_directory is not None:
            self.download_status_var.set("Downloading...")
            download_thread = threading.Thread(target=self.download_and_install, args=(workshop_id, game_directory), daemon=True)
            download_thread.start()
            self.after(100, self.check_download_status, download_thread, workshop_id)
            
    def check_download_status(self, download_thread, workshop_id):
        if download_thread.is_alive():
            self.update_download_size(workshop_id)
            self.after(1000, self.check_download_status, download_thread, workshop_id)
        else:
            self.download_status.configure(text="Download completed!")
            self.download_size_var.set("")

    def download_and_install(self, workshop_id, game_directory):
        self.after_idle(self.download_status_var.set, "Downloading...")
        self.download_workshop_item(workshop_id)
        folder_name = self.get_folder_name(workshop_id)
        self.install_files(workshop_id, folder_name, game_directory)

        self.show_success_message(workshop_id, folder_name, game_directory)
        
    def show_success_message(self, workshop_id, folder_name, game_directory):
        self.download_status_var.set("Download completed!")
        messagebox.showinfo("Success", "Installation completed!")
        view_folder = messagebox.askyesno("View folder", "Do you want to open the created folder?")
        if view_folder:
            os.startfile(os.path.join(game_directory, "usermaps", folder_name))

        self.after(5000, self.clear_download_status)
            
    def clear_download_status(self):
        self.download_status_var.set("")
                
    def add_credits(self):
        credits_text = "Created by Alexandre Hemery -"
        github_text = "Github"
    
        self.credits_label = tk.Label(self.bottom_frame, text=credits_text, font=("TkDefaultFont", 8))
        self.credits_label.pack(side=tk.LEFT, anchor="sw")

        self.github_link = tk.Label(self.bottom_frame, text=github_text, font=("TkDefaultFont", 8), fg="blue", cursor="hand2")
        self.github_link.pack(side=tk.LEFT, anchor="sw")
        self.github_link.bind("<Button-1>", self.open_github)
        
    def open_github(self, event):
        webbrowser.open("https://github.com/alexandre-hemery/bo3-cm-maps-installer")
        
    def add_version(self):
        version_text = "- V. 1.3"
        changelog_text = "Changelog"

        self.version_label = tk.Label(self.bottom_frame, text=version_text, font=("TkDefaultFont", 8))
        self.version_label.pack(side=tk.RIGHT, anchor="se")

        self.changelog_link = tk.Label(self.bottom_frame, text=changelog_text, font=("TkDefaultFont", 8), fg="blue", cursor="hand2")
        self.changelog_link.pack(side=tk.RIGHT, anchor="se")
        self.changelog_link.bind("<Button-1>", self.open_changelog)
        
    def open_changelog(self, event):
        webbrowser.open("https://github.com/alexandre-hemery/bo3-cm-maps-installer/releases/tag/release-1.3")
        
    def delete_files(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))

        for root, dirs, files in os.walk(current_directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file != os.path.basename(__file__) and file != 'steamcmd.exe' and file != 'game_directory.txt':
                    os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)

    def confirm_delete(self):
        confirmation = messagebox.askyesno("Confirmation", "This action will delete all files and folders in the directory, except for the script, steamcmd.exe, and the 'game_directory.txt' file that allows the program to remember the game directory. We kindly ask you to use this feature only for debugging purposes, in cases where steamcmd.exe is being stubborn and refuses to download the requested item despite multiple attempts. Upon the next execution of the program, steamcmd.exe will download its essential files as if it were its first use. Do you want to proceed?")
        if confirmation:
            self.delete_files()
            messagebox.showinfo("Success", "The files and folders have been deleted.")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
