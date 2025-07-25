import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, font
from special_characters import check_allowed_characters, ALLOWED_CHARS
from language_check import fix_mixed_letters, detect_language

excel_df = None  # Глобальная переменная для хранения последнего загруженного DataFrame

def remove_special_characters(text):
    return ''.join(ch for ch in str(text) if ch in ALLOWED_CHARS or ch == "\n")

def highlight_text_with_specials(text):
    # Возвращает список (часть, is_special) для форматированного вывода
    result = []
    buf = ''
    for ch in text:
        if ch not in ALLOWED_CHARS and ch != "\n":
            if buf:
                result.append((buf, False))
                buf = ''
            result.append((f'[!{ch}!]', True))
        else:
            buf += ch
    if buf:
        result.append((buf, False))
    return result

def highlight_specials(text):
    text_input.tag_remove("special", "1.0", tk.END)
    for i, ch in enumerate(text):
        if ch not in ALLOWED_CHARS:
            start = f"1.0+{i}c"
            end = f"1.0+{i+1}c"
            text_input.tag_add("special", start, end)
    text_input.tag_config("special", foreground="#e53935")

def on_remove_specials_excel():
    global excel_df
    if excel_df is None:
        messagebox.showwarning("Нет данных", "Сначала выберите Excel-файл для обработки.")
        return
    new_df = excel_df.copy()
    # Удаляем спецсимволы и заменяем смешанные буквы
    new_df.iloc[:, 0] = new_df.iloc[:, 0].apply(lambda x: remove_special_characters(fix_mixed_letters(x)))
    excel_df = new_df
    messagebox.showinfo("Готово", "Все спецсимволы удалены и смешанные буквы заменены в первой колонке. Для сохранения используйте кнопку 'Скачать таблицу'.")

def on_save_excel():
    global excel_df
    if excel_df is None:
        messagebox.showwarning("Нет данных", "Сначала выберите Excel-файл для обработки.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Сохранить таблицу как")
    if not save_path:
        return
    try:
        excel_df.to_excel(save_path, index=False, header=False)
        messagebox.showinfo("Сохранено", f"Таблица успешно сохранена по пути:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

def on_check_excel():
    global excel_df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not file_path:
        return
    try:
        df = pd.read_excel(file_path, header=None)
        excel_df = df.copy()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
        return
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    for idx, val in enumerate(df.iloc[:, 0]):
        if not isinstance(val, str):
            val = str(val)
        allowed, _ = check_allowed_characters(val)
        if allowed:
            continue
        result_text.insert(tk.END, f'Строка {idx+1}: ', "warn")
        for part, is_special in highlight_text_with_specials(val):
            tag = "special" if is_special else "normal"
            result_text.insert(tk.END, part, tag)
        result_text.insert(tk.END, "\n", "normal")
    result_text.config(state="disabled")
    messagebox.showinfo("Проверка завершена", "Проверка файла завершена. Результаты отображены ниже.")

def on_check_special():
    text = text_input.get("1.0", tk.END)
    # Убираем лишний перевод строки в конце, который всегда есть у Text
    if text.endswith("\n"):
        text = text[:-1]
    specials = [(i, ch) for i, ch in enumerate(text) if ch not in ALLOWED_CHARS and ch != "\n"]
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    if not specials:
        result_text.insert(tk.END, "Спецсимволов не найдено", "ok")
    else:
        result_text.insert(tk.END, "В тексте присутствует спецсимвол(ы):\n", "warn")
        # Формируем вывод с подсветкой спецсимволов
        for part, is_special in highlight_text_with_specials(text):
            tag = "special" if is_special else "normal"
            result_text.insert(tk.END, part, tag)
    result_text.config(state="disabled")


def on_check_language():
    text = text_input.get("1.0", tk.END)
    words = text.split()
    incorrect = []
    fixed_words = []
    text_input.tag_remove("lang_error", "1.0", tk.END)
    for word in words:
        fixed = fix_mixed_letters(word)
        if word != fixed:
            incorrect.append((word, fixed))
            fixed_words.append(fixed)
        else:
            fixed_words.append(word)
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    if not incorrect:
        result_text.insert(tk.END, "Весь текст прошёл проверку на язык и смешанные буквы", "ok")
    else:
        msg = "Обнаружены слова с ошибками:\n" + "\n".join([f'"{w}" → "{f}"' for w, f in incorrect])
        result_text.insert(tk.END, msg, "warn")
    result_text.config(state="disabled")
    highlight_specials(text)


def on_paste(event=None):
    try:
        clipboard = root.clipboard_get()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, clipboard)
    except Exception:
        messagebox.showerror("Ошибка", "Не удалось вставить текст из буфера обмена.")
    return "break"


def run_app():
    global text_input, result_text, root
    root = tk.Tk()
    root.title("Проверка текста")
    root.geometry("800x500")
    root.configure(bg="#f5f5f5")

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=12)

    label = tk.Label(root, text="Введите текст для проверки:", bg="#f5f5f5", font=("Segoe UI", 12, "bold"))
    label.pack(pady=(15, 5))

    text_input = tk.Text(root, height=6, width=90, font=("Consolas", 13), wrap="word", borderwidth=2, relief="groove")
    text_input.pack(pady=5)
    text_input.bind("<Control-v>", on_paste)
    text_input.bind("<Control-V>", on_paste)

    paste_btn = tk.Button(root, text="Вставить из буфера", command=on_paste, bg="#1976d2", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#1565c0", activeforeground="white")
    paste_btn.pack(pady=2)

    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=12)

    check_special_btn = tk.Button(btn_frame, text="Проверить на спецсимволы", command=on_check_special, bg="#00897b", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#00695c", activeforeground="white")
    check_special_btn.pack(side="left", padx=12)

    check_lang_btn = tk.Button(btn_frame, text="Проверить на язык", command=on_check_language, bg="#3949ab", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#283593", activeforeground="white")
    check_lang_btn.pack(side="left", padx=12)

    check_excel_btn = tk.Button(btn_frame, text="Проверить Excel-файл", command=on_check_excel, bg="#fbc02d", fg="#222", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#f9a825", activeforeground="#222")
    check_excel_btn.pack(side="left", padx=12)

    # Кнопки для удаления спецсимволов и сохранения Excel
    remove_btn = tk.Button(root, text="Удалить спецсимволы в таблице", command=on_remove_specials_excel, bg="#d84315", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#b71c1c", activeforeground="white")
    remove_btn.pack(pady=2)
    save_btn = tk.Button(root, text="Скачать таблицу", command=on_save_excel, bg="#43a047", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#2e7d32", activeforeground="white")
    save_btn.pack(pady=2)

    result_text = tk.Text(root, height=20, width=120, wrap="word", borderwidth=2, relief="flat", font=("Consolas", 13))
    result_text.pack(pady=10)
    result_text.tag_configure("special", foreground="#e53935")
    result_text.tag_configure("normal", foreground="#222222")
    result_text.tag_configure("ok", foreground="#43a047", font=("Segoe UI", 12, "bold"))
    result_text.tag_configure("warn", foreground="#e53935", font=("Segoe UI", 12, "bold"))
    result_text.config(state="disabled")

    root.mainloop()
