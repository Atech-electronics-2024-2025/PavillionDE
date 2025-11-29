import tkinter as tk
import subprocess
import os
import pygame

os.system("pulseaudio --start")
def play_startup_sound():
    sound_path = "/usr/share/pavillion/start.wav"
    os.system(f"aplay {sound_path} &")  # & runs it in background

# === Desktop Environment Window ===
root = tk.Tk()
root.title("Pavillion DE")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

# OS/2 Warp 4 blue desktop background
root.configure(bg="#3A6EA5")
root.attributes("-fullscreen", True)

# === Top Panel (OS/2 3D Gray) ===
panel = tk.Frame(root, bg="#C0C0C0", height=32, bd=2, relief="raised")
panel.pack(fill="x", side="top")


# === Menus (OS/2 look) ===
def run_app(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print("Error:", e)

menu_fg = "black"
menu_bg = "#E0E0E0"   # OS/2 light gray

btn_apps = tk.Menubutton(panel, text="Applications", bg="#C0C0C0",
                          fg="black", relief="flat", font=("MS Sans Serif", 10))
btn_menu = tk.Menu(btn_apps, tearoff=0, bg=menu_bg, fg=menu_fg, font=("MS Sans Serif", 10))

btn_menu.add_command(label="Terminal (xterm)", command=lambda: run_app("xterm"))
btn_menu.add_command(label="File Manager (nautilus)", command=lambda: run_app("nautilus"))
btn_menu.add_separator()
btn_menu.add_command(label="Quit Desktop", command=root.destroy)

btn_apps.config(menu=btn_menu)
btn_apps.pack(side="left", padx=6)

btn_places = tk.Button(panel, text="Places", bg="#C0C0C0", fg="black",
                       relief="flat", font=("MS Sans Serif", 10))
btn_places.pack(side="left", padx=6)

btn_system = tk.Button(panel, text="System", bg="#C0C0C0", fg="black",
                       relief="flat", font=("MS Sans Serif", 10))
btn_system.pack(side="left", padx=6)

# === Fake Taskbar (bottom, OS/2 style) ===
taskbar = tk.Frame(root, bg="#A0A0A0", height=30, bd=2, relief="sunken")
taskbar.pack(fill="x", side="bottom")

lbl = tk.Label(taskbar, text="Pavillion DE – Version 1.0 Beta",
               fg="black", bg="#A0A0A0", font=("MS Sans Serif", 9))
lbl.pack(side="left", padx=10)

root.after(1000, play_startup_sound)

# === Main Loop ===
root.mainloop()
