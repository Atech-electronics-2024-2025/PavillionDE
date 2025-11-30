import tkinter as tk
import subprocess
import os
import pygame
import time 
os.system("pulseaudio --start")
def play_startup_sound():
    sound_path = "/usr/share/pavillion/start.wav"
    os.system(f"aplay {sound_path} &")  # & runs it in background

# === Desktop Environment Window ===
root = tk.Tk()
root.title("Pavillion DE")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.configure(cursor="arrow")

# OS/2 Warp 4 blue desktop background
root.configure(bg="#3A6EA5")
root.attributes("-fullscreen", True)

# === Top Panel (OS/2 3D Gray) ===
panel = tk.Frame(root, bg="#C0C0C0", height=32, bd=2, relief="raised")
panel.pack(fill="x", side="top")

def update_clock():
    current = time.strftime("%H:%M:%S")
    lbl_clock.config(text=current)
    root.after(1000, update_clock)
def shutdown_system():
    subprocess.Popen("systemctl poweroff", shell=True)

def reboot_system():
    subprocess.Popen("systemctl reboot", shell=True)

def logout_pavillion():
    root.destroy()


def open_run_dialog():
    win = tk.Toplevel(root)
    win.title("Run")
    win.geometry("300x100")
    win.configure(bg="#D0D0D0")

    entry = tk.Entry(win)
    entry.pack(pady=10, padx=10)

    def run_now():
        run_app(entry.get())
        win.destroy()

    tk.Button(win, text="Run", command=run_now).pack(pady=5)
def create_desktop_icon(text, command, x, y):
    icon = tk.Button(
        root,
        text=text,
        width=12,
        height=4,
        bg="#4C84D3",
        fg="white",
        relief="flat",
        command=lambda: run_app(command)
    )
    icon.place(x=x, y=y)

    # Drag & drop
    def start_drag(e):
        icon.startX = e.x
        icon.startY = e.y

    def drag(e):
        new_x = icon.winfo_x() + (e.x - icon.startX)
        new_y = icon.winfo_y() + (e.y - icon.startY)
        icon.place(x=new_x, y=new_y)

    icon.bind("<ButtonPress-1>", start_drag)
    icon.bind("<B1-Motion>", drag)

    return icon
def load_apps(menu_widget):
    import configparser, glob

    desktop_dirs = [
        "/usr/share/applications",
        os.path.expanduser("~/.local/share/applications")
    ]

    apps = []

    for directory in desktop_dirs:
        for file in glob.glob(os.path.join(directory, "*.desktop")):
            parser = configparser.ConfigParser(strict=False)
            try:
                parser.read(file)
                name = parser.get("Desktop Entry", "Name", fallback=None)
                exec_cmd = parser.get("Desktop Entry", "Exec", fallback=None)

                if not name or not exec_cmd:
                    continue

                # clean arguments (%U, %F...)
                for symbol in ["%U", "%F", "%u", "%f", "%1", "%2"]:
                    exec_cmd = exec_cmd.replace(symbol, "")

                apps.append((name, exec_cmd.strip()))

            except:
                pass

    apps.sort(key=lambda x: x[0].lower())

    for name, cmd in apps:
        menu_widget.add_command(
            label=name,
            command=lambda c=cmd: run_app(c)
        )

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

btn_system = tk.Menubutton(panel, text="System", bg="#C0C0C0", fg="black",
                           relief="flat", font=("MS Sans Serif", 10))
btn_system.pack(side="left", padx=6)

# === Fake Taskbar (bottom, OS/2 style) ===
taskbar = tk.Frame(root, bg="#A0A0A0", height=30, bd=2, relief="sunken")
taskbar.pack(fill="x", side="bottom")

lbl = tk.Label(taskbar, text="Pavillion DE – Version 1.0 Beta",
               fg="black", bg="#A0A0A0", font=("MS Sans Serif", 9))
lbl.pack(side="left", padx=10)

root.after(1000, play_startup_sound)
lbl_clock = tk.Label(panel, text="", fg="white", bg="black", font=("Ubuntu", 12))
lbl_clock.pack(side="right", padx=10)

update_clock()
btn_system_menu = tk.Menu(btn_system, tearoff=0)
btn_system_menu.add_command(label="Shutdown", command=shutdown_system)
btn_system_menu.add_command(label="Restart", command=reboot_system)
btn_system_menu.add_command(label="Logout", command=logout_pavillion)
btn_system.config(menu=btn_system_menu)
open_run_dialog()

create_desktop_icon("Terminal", "xterm", 20, 80)
load_apps(btn_menu)

# === Main Loop ===
root.mainloop()
