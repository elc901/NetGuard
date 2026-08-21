import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import subprocess
import sys

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

BLOCKED_DOMAINS = [
    "max.ru",
]

MARKER_START = "# NetGuard START"
MARKER_END = "# NetGuard END"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def read_hosts():
    with open(HOSTS_PATH, "r", encoding="utf-8") as file:
        return file.read()


def write_hosts(content):
    with open(HOSTS_PATH, "w", encoding="utf-8") as file:
        file.write(content)


def enable_block():
    hosts = read_hosts()

    # Если блок уже существует — ничего не делаем
    if MARKER_START in hosts:
        update_status(True)
        return

    block = "\n" + MARKER_START + "\n"

    for domain in BLOCKED_DOMAINS:
        block += f"127.0.0.1 {domain}\n"

    block += MARKER_END + "\n"

    write_hosts(hosts.rstrip() + block)

    flush_dns()
    update_status(True)


def disable_block():
    hosts = read_hosts()

    start = hosts.find(MARKER_START)

    if start == -1:
        update_status(False)
        return

    end = hosts.find(MARKER_END, start)

    if end == -1:
        messagebox.showerror(
            "Ошибка",
            "Повреждён блок NetGuard в hosts."
        )
        return

    end += len(MARKER_END)

    new_hosts = hosts[:start] + hosts[end:]

    write_hosts(new_hosts)

    flush_dns()
    update_status(False)


def flush_dns():
    try:
        subprocess.run(
            ["ipconfig", "/flushdns"],
            capture_output=True,
            text=True
        )
    except:
        pass


def update_status(enabled):
    if enabled:
        status_label.config(
            text="Статус: 🟢 Защита включена"
        )
    else:
        status_label.config(
            text="Статус: 🔴 Защита выключена"
        )


def enable_clicked():
    try:
        enable_block()
        messagebox.showinfo(
            "NetGuard",
            "Блокировка включена."
        )
    except PermissionError:
        messagebox.showerror(
            "Недостаточно прав",
            "Запустите программу от имени администратора."
        )
    except Exception as error:
        messagebox.showerror(
            "Ошибка",
            str(error)
        )


def disable_clicked():
    try:
        disable_block()
        messagebox.showinfo(
            "NetGuard",
            "Блокировка выключена."
        )
    except PermissionError:
        messagebox.showerror(
            "Недостаточно прав",
            "Запустите программу от имени администратора."
        )
    except Exception as error:
        messagebox.showerror(
            "Ошибка",
            str(error)
        )


# -------------------------
# Проверяем права
# -------------------------

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(f'"{arg}"' for arg in sys.argv),
        None,
        1
    )
    raise SystemExit


# -------------------------
# Создаём окно
# -------------------------

root = tk.Tk()

root.title("NetGuard")
root.geometry("420x300")
root.resizable(False, False)


title = tk.Label(
    root,
    text="NetGuard",
    font=("Segoe UI", 22, "bold")
)

title.pack(pady=(25, 5))


description = tk.Label(
    root,
    text="Управление сетевой блокировкой",
    font=("Segoe UI", 10)
)

description.pack()


status_label = tk.Label(
    root,
    text="Статус: 🔴 Защита выключена",
    font=("Segoe UI", 12, "bold")
)

status_label.pack(pady=25)


enable_button = tk.Button(
    root,
    text="Включить",
    width=15,
    height=2,
    command=enable_clicked
)

enable_button.pack(pady=5)


disable_button = tk.Button(
    root,
    text="Выключить",
    width=15,
    height=2,
    command=disable_clicked
)

disable_button.pack(pady=5)


sites_label = tk.Label(
    root,
    text="Заблокированные домены:\n"
         + "\n".join(BLOCKED_DOMAINS),
    font=("Segoe UI", 9),
    justify="center"
)

sites_label.pack(pady=15)


root.mainloop()