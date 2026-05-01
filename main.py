import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "books.json"

# ===== Работа с JSON =====
def load_books():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_books():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# ===== Логика =====
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Страницы должны быть числом!")
        return

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages),
        "read": False
    }

    books.append(book)
    save_books()
    update_table()
    clear_fields()

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите книгу!")
        return

    index = int(selected[0])
    del books[index]
    save_books()
    update_table()

def toggle_read():
    selected = tree.selection()
    if not selected:
        return

    index = int(selected[0])
    books[index]["read"] = not books[index]["read"]
    save_books()
    update_table()

def search_books():
    query = entry_search.get().lower()
    filtered = [b for b in books if query in b["title"].lower()]
    update_table(filtered)

def filter_genre():
    genre = entry_filter_genre.get().lower()
    filtered = [b for b in books if genre in b["genre"].lower()]
    update_table(filtered)

def filter_pages():
    value = entry_filter_pages.get()

    if not value.isdigit():
        messagebox.showerror("Ошибка", "Введите число!")
        return

    value = int(value)
    filtered = [b for b in books if b["pages"] > value]
    update_table(filtered)

def sort_books():
    key = sort_var.get()

    if key == "Название":
        books.sort(key=lambda x: x["title"])
    elif key == "Автор":
        books.sort(key=lambda x: x["author"])
    elif key == "Страницы":
        books.sort(key=lambda x: x["pages"])

    update_table()

def show_all():
    update_table()

def clear_fields():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def update_table(data=None):
    for row in tree.get_children():
        tree.delete(row)

    data = data if data else books

    for i, book in enumerate(data):
        status = "✔" if book["read"] else "✘"
        tree.insert("", "end", iid=i, values=(
            book["title"],
            book["author"],
            book["genre"],
            book["pages"],
            status
        ))

# ===== GUI =====
root = tk.Tk()
root.title("Book Tracker PRO")
root.geometry("800x600")

books = load_books()

# --- Ввод ---
frame_input = ttk.LabelFrame(root, text="Добавить книгу")
frame_input.pack(fill="x", padx=10, pady=5)

entry_title = ttk.Entry(frame_input)
entry_author = ttk.Entry(frame_input)
entry_genre = ttk.Entry(frame_input)
entry_pages = ttk.Entry(frame_input)

ttk.Label(frame_input, text="Название").grid(row=0, column=0)
ttk.Label(frame_input, text="Автор").grid(row=0, column=1)
ttk.Label(frame_input, text="Жанр").grid(row=0, column=2)
ttk.Label(frame_input, text="Страницы").grid(row=0, column=3)

entry_title.grid(row=1, column=0)
entry_author.grid(row=1, column=1)
entry_genre.grid(row=1, column=2)
entry_pages.grid(row=1, column=3)

ttk.Button(frame_input, text="Добавить", command=add_book).grid(row=1, column=4, padx=5)

# --- Фильтры ---
frame_filter = ttk.LabelFrame(root, text="Фильтры")
frame_filter.pack(fill="x", padx=10, pady=5)

entry_filter_genre = ttk.Entry(frame_filter)
entry_filter_pages = ttk.Entry(frame_filter)
entry_search = ttk.Entry(frame_filter)

ttk.Label(frame_filter, text="Жанр").grid(row=0, column=0)
entry_filter_genre.grid(row=0, column=1)

ttk.Button(frame_filter, text="Фильтр", command=filter_genre).grid(row=0, column=2)

ttk.Label(frame_filter, text="Страницы >").grid(row=0, column=3)
entry_filter_pages.grid(row=0, column=4)

ttk.Button(frame_filter, text="Фильтр", command=filter_pages).grid(row=0, column=5)

ttk.Label(frame_filter, text="Поиск").grid(row=1, column=0)
entry_search.grid(row=1, column=1)

ttk.Button(frame_filter, text="Найти", command=search_books).grid(row=1, column=2)

ttk.Button(frame_filter, text="Показать всё", command=show_all).grid(row=1, column=3)

# --- Сортировка ---
sort_var = tk.StringVar(value="Название")

ttk.Combobox(frame_filter, textvariable=sort_var, values=[
    "Название", "Автор", "Страницы"
]).grid(row=1, column=4)

ttk.Button(frame_filter, text="Сортировать", command=sort_books).grid(row=1, column=5)

# --- Таблица ---
columns = ("Название", "Автор", "Жанр", "Страницы", "Прочитано")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# --- Кнопки ---
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Удалить", command=delete_book).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Прочитано / Не прочитано", command=toggle_read).grid(row=0, column=1, padx=5)

update_table()

root.mainloop()
