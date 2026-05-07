import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("900x600")

        self.records = []

        # ===== Поля ввода =====
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Температура:").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(input_frame)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        self.precipitation_var = tk.BooleanVar()
        tk.Checkbutton(
            input_frame,
            text="Осадки",
            variable=self.precipitation_var
        ).grid(row=3, column=1, sticky="w")

        tk.Button(
            input_frame,
            text="Добавить запись",
            command=self.add_record,
            bg="lightgreen"
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # ===== Фильтрация =====
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Дата:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            filter_frame,
            text="Фильтр по дате",
            command=self.filter_by_date
        ).grid(row=0, column=2, padx=5)

        tk.Label(filter_frame, text="Температура выше:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_temp_entry = tk.Entry(filter_frame)
        self.filter_temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            filter_frame,
            text="Фильтр по температуре",
            command=self.filter_by_temperature
        ).grid(row=1, column=2, padx=5)

        tk.Button(
            filter_frame,
            text="Показать все",
            command=self.display_records
        ).grid(row=2, column=1, pady=5)

        # ===== Таблица =====
        columns = ("date", "temperature", "description", "precipitation")

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== Кнопки сохранения =====
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Сохранить JSON",
            command=self.save_to_json,
            bg="lightblue"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            buttons_frame,
            text="Загрузить JSON",
            command=self.load_from_json,
            bg="lightyellow"
        ).grid(row=0, column=1, padx=10)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        description = self.desc_entry.get()
        precipitation = "Да" if self.precipitation_var.get() else "Нет"

        if not self.validate_date(date):
            messagebox.showerror(
                "Ошибка",
                "Дата должна быть в формате YYYY-MM-DD"
            )
            return

        try:
            temp = float(temp)
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Температура должна быть числом"
            )
            return

        if description.strip() == "":
            messagebox.showerror(
                "Ошибка",
                "Описание не должно быть пустым"
            )
            return

        record = {
            "date": date,
            "temperature": temp,
            "description": description,
            "precipitation": precipitation
        }

        self.records.append(record)
        self.display_records()
        self.clear_inputs()

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)

    def display_records(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            records = self.records

        for record in records:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    record["date"],
                    record["temperature"],
                    record["description"],
                    record["precipitation"]
                )
            )

    def filter_by_date(self):
        filter_date = self.filter_date_entry.get()

        filtered = [
            record for record in self.records
            if record["date"] == filter_date
        ]

        self.display_records(filtered)

    def filter_by_temperature(self):
        try:
            temp_value = float(self.filter_temp_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Введите число для фильтра температуры"
            )
            return

        filtered = [
            record for record in self.records
            if record["temperature"] > temp_value
        ]

        self.display_records(filtered)

    def save_to_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.records,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            messagebox.showinfo(
                "Успех",
                "Данные успешно сохранены"
            )

    def load_from_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.records = json.load(file)

            self.display_records()

            messagebox.showinfo(
                "Успех",
                "Данные успешно загружены"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
