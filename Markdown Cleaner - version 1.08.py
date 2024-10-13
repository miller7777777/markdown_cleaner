import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import html
from tkinter import ttk


class MarkdownProcessor:
    def __init__(self, master):
        self.master = master
        master.title("Markdown Cleaner - version 1.08")

        # Установка размеров окна и цветовой схемы Solarized Dark
        master.geometry("600x220")
        master.configure(bg="#002b36")  # Темный фон Solarized

        # Кнопка для выбора папки с увеличенным размером и стилями
        self.select_folder_button = ttk.Button(
            master, text="Выбрать папку", command=self.select_folder
        )
        self.select_folder_button.pack(pady=20, padx=10)
        self.select_folder_button["style"] = "Solarized.TButton"  # Добавление стиля

        # Кнопка для запуска обработки
        self.run_button = ttk.Button(
            master, text="Run", command=self.process_markdown_files
        )
        self.run_button.pack(pady=20, padx=10)
        self.run_button["style"] = "Solarized.TButton"

        # Стиль для кнопок
        style = ttk.Style()
        style.configure(
            "Solarized.TButton",
            background="#586e75",
            foreground="#000000",  # Черный цвет текста
            padding=10,  # Увеличенный размер кнопок
            relief="raised",
            borderwidth=5,
            font=("Arial", 10, "bold"),
        )  # Используем жирный шрифт

        self.folder_path = ""
        self.found_files = 0
        self.processed_files = 0

        # Текст с авторством внизу
        self.copyright_label = tk.Label(
            master, text="© 2024 Miller777 & Chat GPT", bg="#002b36", fg="#839496"
        )
        self.copyright_label.pack(side=tk.BOTTOM, pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            messagebox.showinfo("Выбор папки", f"Выбрана папка: {self.folder_path}")

    def process_markdown_files(self):
        if not self.folder_path:
            messagebox.showwarning("Ошибка", "Сначала выберите папку!")
            return

        self.found_files = 0
        self.processed_files = 0

        for root, dirs, files in os.walk(self.folder_path):  # Рекурсивный обход папок
            for filename in files:
                if filename.endswith(".md"):
                    self.found_files += 1
                    file_path = os.path.join(root, filename)

                    # Чтение содержимого оригинального файла
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    # Удаляем HTML-теги и заменяем специальные символы
                    cleaned_content = self.remove_html_tags(content)
                    cleaned_content = self.replace_special_html_entities(
                        cleaned_content
                    )

                    # Сохраняем очищенный файл только если содержимое изменилось
                    if (
                        cleaned_content != content
                    ):  # Сравниваем оригинал и очищенный контент
                        backup_path = file_path + ".bak"

                        # Создаем резервную копию
                        with open(backup_path, "w", encoding="utf-8") as backup_file:
                            backup_file.write(content)

                        # Записываем очищенный контент в оригинальный файл
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(cleaned_content)
                        self.processed_files += (
                            1  # Увеличиваем счетчик обработанных файлов
                        )

        # Уведомляем пользователя
        messagebox.showinfo(
            "Завершено",
            f"Найдено файлов: {self.found_files}\nОбработано файлов: {self.processed_files}",
        )

    def remove_html_tags(self, text):
        clean = re.compile(r"&lt;.*?&gt;")
        return re.sub(clean, "", text)

    def replace_special_html_entities(self, text):
        # Заменяем символы на соответствующие им символы
        text = html.unescape(text)
        return text


if __name__ == "__main__":
    root = tk.Tk()
    markdown_processor = MarkdownProcessor(root)
    root.mainloop()
