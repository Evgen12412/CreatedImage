import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Устанавливаем начальные размеры окна
        self.root.geometry("800x600")
        self.root.minsize(400, 300)  # Минимальные размеры окна

        # Создаем изображение и холст
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создаем холст с возможностью изменения размеров
        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Холст растягивается на все окно

        # Настройка кисти
        self.size_brush = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(self.size_brush[0])

        self.pen_color = 'black'

        # Настройка интерфейса
        self.setup_ui()

        # Переменные для рисования
        self.last_x, self.last_y = None, None
        self.text_to_draw = None  # Переменная для хранения текста
        self.text_to_draw_size = None  # Переменная для хранения размера текста

        # Привязка событий
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<Control-Button-1>', self.pick_color)
        self.root.bind('<Control-c>', self.choose_color)
        self.root.bind('<Control-s>', self.save_image)

    def setup_ui(self):
        # Создаем фрейм для кнопок
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Кнопка "Очистить"
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Кнопка "Выбрать цвет"
        self.color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        self.color_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Кнопка "Сохранить"
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # OptionMenu для выбора размера кисти
        self.option_menu = tk.OptionMenu(control_frame, self.selected_option, *self.size_brush,
                                         command=self.on_option_select)
        self.option_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Индикатор текущего цвета
        self.current_color_indicator = tk.Label(control_frame, width=5, height=1, bg=self.pen_color)
        self.current_color_indicator.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Кнопка "Размер экрана"
        size_canvas = tk.Button(control_frame, text="Размер экрана", command=self.set_size_window)
        size_canvas.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # Кнопка "Текст"
        text_button = tk.Button(control_frame, text="Текст", command=self.prepare_text)
        text_button.grid(row=0, column=6, padx=5, pady=5, sticky="ew")

        # Кнопка "Фон холста"
        background = tk.Button(control_frame, text="Фон холста", command=self.choose_background)
        background.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Настройка адаптивности для колонок
        for i in range(8):  # 8 колонок в control_frame
            control_frame.grid_columnconfigure(i, weight=1)

    def paint(self, event):
        if self.last_x and self.last_y:
            brush_size = int(self.selected_option.get())
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, e=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_indicator()

    def save_image(self, e=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")



    def pick_color(self, event):
        """
                Метод для выбора цвета пипеткой.
        """
        x, y = event.x, event.y
        if 0 <= x < self.image.width and 0 <= y < self.image.height:
            try:
                color = self.image.getpixel((x, y))
                self.pen_color = "#{:02x}{:02x}{:02x}".format(*color)
                self.update_color_indicator()
            except Exception as e:
                messagebox.showwarning("Ошибка", f"Не удалось получить цвет пикселя: {e}")
        else:
            messagebox.showwarning("Ошибка", "Вы вышли за пределы холста!")

    def update_color_indicator(self):
        self.current_color_indicator.config(bg=self.pen_color)

    def set_size_window(self):
        '''
        Метод открывает окна для ввода размеров
        :return:
        '''
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить размер")
        dialog.geometry("300x250")

        label_width = tk.Label(dialog, text="Ширина:")
        label_width.pack(pady=5)
        self.entry_width = tk.Entry(dialog)
        self.entry_width.pack(pady=5)

        label_height = tk.Label(dialog, text="Высота:")
        label_height.pack(pady=5)
        self.entry_height = tk.Entry(dialog)
        self.entry_height.pack(pady=5)

        apply_button = tk.Button(dialog, text="Применить", command=self.apply_size)
        apply_button.pack(pady=10)

        close_button = tk.Button(dialog, text="Закрыть", command=dialog.destroy)
        close_button.pack(pady=5)

    def apply_size(self):
        '''
                метод задает полученные размеры окну
                :return:
        '''
        width = self.entry_width.get()
        height = self.entry_height.get()

        if width.isdigit() and height.isdigit() and int(width) > 0 and int(height) > 0:
            width = int(width)
            height = int(height)

            self.canvas.config(width=width, height=height)
            self.image = Image.new("RGB", (width, height), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.clear_canvas()
        else:
            messagebox.showerror("Ошибка", "Ширина и высота должны быть положительными числами!")

    def prepare_text(self):
        '''
        получаем данные от пользователя
        :return:
        '''
        # Открываем диалоговое окно для ввода текста
        self.text_to_draw = simpledialog.askstring("Ввод текста", "Введите текст:")
        if self.text_to_draw:
            # Открываем диалоговое окно для ввода размера текста
            self.text_to_draw_size = simpledialog.askstring("Ввод размера текста", "Введите размер текста:")
            if self.text_to_draw_size and self.text_to_draw_size.isdigit():
                # Переключаем обработчик клика для добавления текста
                self.canvas.bind('<Button-1>', self.add_text)
            else:
                messagebox.showwarning("Ошибка", "Размер текста должен быть числом!")

    def add_text(self, event):
        '''
        Добавление текста в окно
        :param event:
        :return:
        '''
        # Добавляем текст на изображение и холст
        if self.text_to_draw and self.text_to_draw_size:
            x, y = event.x, event.y
            font_size = int(self.text_to_draw_size)
            try:
                # Используем системный шрифт
                font = ImageFont.load_default()
                self.draw.text((x, y), self.text_to_draw, fill=self.pen_color, font=font)
                self.canvas.create_text(x, y, text=self.text_to_draw, fill=self.pen_color, font=("Arial", font_size))
            except Exception as e:
                messagebox.showwarning("Ошибка", f"Не удалось добавить текст: {e}")
            finally:
                # Сбрасываем текст и размер
                self.text_to_draw = None
                self.text_to_draw_size = None
                self.canvas.unbind('<Button-1>')  # Возвращаем стандартное поведение клика

    def choose_background(self):
        '''
        Установка фона на холсте
        :return:
        '''
        color_ = colorchooser.askcolor()[1]  # Получаем цвет в формате #RRGGBB
        if color_:
            self.canvas.config(background=color_)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
