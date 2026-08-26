import tkinter as tk
from tkinter import messagebox
import ctypes
import subprocess
import sys

# константы
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
BLOCKED_DOMAINS = []
MARKER_START = "# NetGuard START"
MARKER_END = "# NetGuard END"



def add_domain_from_input(input_label, sites_label):
    domain = input_label.get().strip()
    if domain and domain not in BLOCKED_DOMAINS:
        BLOCKED_DOMAINS.append(domain)
        input_label.delete(0, tk.END)
        sites_label.config(text="Заблокированные домены:\n" + "\n".join(BLOCKED_DOMAINS))
        messagebox.showinfo("Успех", f"Домен {domain} добавлен")
    else:
        messagebox.showwarning("Ошибка", "Домен уже есть или пустой")




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

def enable_guard():
    hosts = read_hosts()
    
    if MARKER_START in hosts:
        return
    
    block = "\n" + MARKER_START + "\n"
    for domain in BLOCKED_DOMAINS:
        block += f"127.0.0.1 {domain}\n"
    block += MARKER_END + "\n"
    
    write_hosts(hosts.rstrip() + block)
    flush_dns()

def disable_guard():
    hosts = read_hosts()
    
    start = hosts.find(MARKER_START)
    if start == -1:
        return
    
    end = hosts.find(MARKER_END, start)
    if end == -1:
        raise Exception("Повреждён блок NetGuard в hosts.")
    
    end += len(MARKER_END)
    new_hosts = hosts[:start] + hosts[end:]
    write_hosts(new_hosts)
    flush_dns()

def flush_dns(): # сброс кэша DNS
    try:
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
    except:
        pass

# обработка
def enable_clicked(status_label):
    try:
        enable_guard()
        update_status(status_label, True)
        messagebox.showinfo("NetGuard", "Блокировка включена.")
    except PermissionError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора.")
    except Exception as error:
        messagebox.showerror("Ошибка", str(error))

def disable_clicked(status_label):
    try:
        disable_guard()
        update_status(status_label, False)
        messagebox.showinfo("NetGuard", "Блокировка выключена.")
    except PermissionError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора.")
    except Exception as error:
        messagebox.showerror("Ошибка", str(error))

def update_status(status_label, enabled):
    if enabled:
        status_label.config(text="Статус: 🟢 Защита включена")
    else:
        status_label.config(text="Статус: 🔴 Защита выключена")

def check_admin_and_restart():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, 
            " ".join(f'"{arg}"' for arg in sys.argv), 
            None, 1
        )
        raise SystemExit

# создание интерфейса

def create_ui():
    root = tk.Tk()
    root.title("NetGuard")
    root.geometry("420x300")
    root.resizable(False, False)
    
    # Заголовок
    title = tk.Label(root, text="NetGuard", font=("Segoe UI", 22, "bold"))
    title.pack(pady=(25, 5))
    
    # Описание
    description = tk.Label(root, text="Управление сетевой блокировкой", font=("Segoe UI", 10))
    description.pack()
    
    # Статус
    status_label = tk.Label(root, text="Статус: 🔴 Защита выключена", font=("Segoe UI", 12, "bold"))
    status_label.pack(pady=25)
    
    # Кнопки
    enable_button = tk.Button(
        root, text="Включить", width=15, height=2,
        command=lambda: enable_clicked(status_label)
    )
    enable_button.pack(pady=5)
    
    disable_button = tk.Button(
        root, text="Выключить", width=15, height=2,
        command=lambda: disable_clicked(status_label)
    )
    disable_button.pack(pady=5)
    
    # Список доменов
    sites_label = tk.Label(
        root,
        text="Заблокированные домены:\n" + "\n".join(BLOCKED_DOMAINS),
        font=("Segoe UI", 9),
        justify="center"
    )
    sites_label.pack(pady=15)
    
    return root



if __name__ == "__main__":
    check_admin_and_restart()
    root = create_ui()
    root.mainloop()