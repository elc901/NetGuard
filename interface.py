import tkinter as tk
from tkinter import messagebox
from back import *
root = tk.Tk()

root.title("NetGuard")
root.geometry("420x300")
root.resizable(False, False) # запрет на изменение размеров

title_label = tk.Label( # текст сверху
    root,
    text="NetGuard",
    font=("Segoe UI", 22, "bold")
)
title_label.pack(pady=(25, 5))

description_label = tk.Label( # описание
    root,
    text="Управление сетевой блокировкой",
    font=("Segoe UI", 10)
)
description_label.pack()

input_label = tk.Entry( # строка для ввода доменов
    root,
    text="Введите домен для блокировки",
    font=("Segoe UI", 10),
    width=30,
    justify="center"
)
input_label.pack(pady=10)

add_button = tk.Button(
    root,
    text="Добавить домен",
    command=lambda: add_domain_from_input(input_label, sites_label)
)
add_button.pack(pady=5)


status_label = tk.Label( # статус
    root, 
    text="Статус: 🔴 Защита выключена",
    font=("Segoe UI", 12, "bold")
)
status_label.pack()

button_enable = tk.Button(
    root,
    text="Включить",
    width=15,
    height=2,
    command=lambda: enable_clicked(status_label)
)
button_enable.pack()

disable_button = tk.Button(
    root,
    text="Выключить",
    width=15,
    height=2,
    command=lambda: disable_guard(status_label)
)
disable_button.pack(pady=5)

add_button = tk.Button(
    root,
    text="Добавить домен",
    command=lambda: add_domain_from_input()
)
add_button.pack(pady=5)


sites_label = tk.Label(
    root,
    text="Заблокированные домены:\n"
         + "\n".join(BLOCKED_DOMAINS),
    font=("Segoe UI", 9),
    justify="center"
)
sites_label.pack(pady=15)

root.mainloop()