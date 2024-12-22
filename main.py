import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.size_brush = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.selected_option = tk.StringVar(self.root)

        self.selected_option.set(self.size_brush[0])

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.previous_color = 'black'  # Предыдущий цвет кисти
        self.eraser_mode = False  # Режим ластика

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка "Очистить"
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.grid(row=0, column=0, padx=5, pady=5)

        # Кнопка "Выбрать цвет"
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка "Сохранить"
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.grid(row=0, column=2, padx=5, pady=5)

        # OptionMenu для выбора размера кисти
        self.option_menu = tk.OptionMenu(control_frame, self.selected_option, *self.size_brush,
                                         command=self.on_option_select)
        self.option_menu.grid(row=0, column=3, padx=5, pady=5)

        # Clear color
        self.clear_color = tk.Button(control_frame, text="Ластик", command = self.toggle_eraser)
        self.clear_color.grid(row=0, column=4, padx=5, pady=5)

    def paint(self, event):
        if self.last_x and self.last_y:
            # Получаем размер кисти из выбранного значения OptionMenu
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
        '''
        Очистка окна
        :return:
        '''
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        '''
        Выбор цвета кисти
        :return:
        '''
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        '''
        Сохранение в файл
        :return:
        '''
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def on_option_select(self, value):
        pass

    def toggle_eraser(self):
        '''
        Функция переключает режим кисти
        :return:
        '''
        if self.eraser_mode:
            # Выходим из режима ластика
            self.pen_color = self.previous_color  # Возвращаем предыдущий цвет
            self.eraser_mode = False
            self.clear_color.configure(bg='SystemButtonFace', text="Ластик")  # Сбрасываем цвет кнопки
        else:
            # Включаем режим ластика
            self.previous_color = self.pen_color  # Сохраняем текущий цвет
            self.pen_color = 'white'  # Устанавливаем белый цвет
            self.eraser_mode = True
            self.clear_color.configure(bg='green', text="Рисовать")



def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
