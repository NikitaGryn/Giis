
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import time


class PaintApp(tk.Tk):
    # Приложение для рисования графических фигур.

    def __init__(self):
        # Инициализация графического редактора.
        super().__init__()

        self.title("Графический редактор")
        self.geometry("800x550")  # Размер окна

        self.draw_area_width = 600
        self.draw_area_height = 400
        self.is_debugging = False
        self.debug_pause = 10
        self.selected_color = "black"  # Цвет фигур
        self.is_drawing = False
        self.selected_figure = "Окружность"  # Тип фигуры по умолчанию
        self.grid_visible = True
        self.grid_step = 10

        self._setup_ui()
        self._center_window()
        self._draw_grid()  # Сетка при запуске

    def _center_window(self):
        # Размещает окно приложения в центре экрана.
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x_coord = (screen_width // 2) - (window_width // 2)
        y_coord = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

    def _draw_grid(self):
        # Отображает сетку на холсте.
        if self.grid_visible:
            for i in range(self.grid_step, self.draw_area_width, self.grid_step):
                self.canvas.create_line(i, 0, i, self.draw_area_height, fill="lightgray", tags="grid_line")
            for i in range(self.grid_step, self.draw_area_height, self.grid_step):
                self.canvas.create_line(0, i, self.draw_area_width, i, fill="lightgray", tags="grid_line")

    def clear_canvas(self):
        # Очищает холст от всех изображений и перерисовывает сетку.
        self.canvas.delete("all")
        self._draw_grid()

    def draw_point(self, x, y):
        # Рисует единичную точку на холсте.
        self.canvas.create_oval(x, y, x + 1, y + 1, fill=self.selected_color, outline="")
        if self.is_debugging:
            print(f"{self.selected_figure.capitalize()}: (x={x}, y={y})")
        self._pause_if_debugging()

    def draw_circle(self, x0, y0, radius):
        x, y, delta = 0, radius, 3 - 2 * radius # дельта для контроля изменения координаты y
        while x <= y:
            for dx, dy in [(x, y), (y, x), (-y, x), (-x, y), (-x, -y), (-y, -x), (y, -x), (x, -y)]:
                self.draw_point(x0 + dx, y0 + dy) # # Рисуем симметричные точки окружности
            x += 1 # Увеличиваем x для перехода к следующей точке по окружности
            if delta > 0: # Если delta больше 0, уменьшаем y и обновляем delta
                y -= 1
                delta += 4 * (x - y) + 10 # Обновляем delta с учетом изменения x и y
            else:
                delta += 4 * x + 6 # Если delta меньше или равно 0, просто обновляем delta

    def draw_ellipse(self, x0, y0, a, b):
        x, y = 0, b
        d1 = b ** 2 - a ** 2 * b + 0.25 * a ** 2 # Значение d1 чтобы понять нужно ли уменьшать y на следующем шаге рисования.
        # Рисование верхней части эллипса
        while (a ** 2) * (y - 0.5) > (b ** 2) * (x + 1):
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y)]: # Рисуем симметричные точки эллипса
                self.draw_point(x0 + dx, y0 + dy)
            x += 1 # Увеличиваем x для перехода к следующей точке
            if d1 < 0:
                d1 += (2 * b ** 2) * x + b ** 2 # Если d1 меньше 0, y остается прежним, обновляем d1
            else: # Если d1 больше или равен 0, уменьшаем y и обновляем d1
                y -= 1
                d1 += (2 * b ** 2) * x - (2 * a ** 2) * y + b ** 2
# Значение d2 используется чтобы понять нужно ли увеличивать x на следующем шаге
        d2 = b ** 2 * (x + 0.5) ** 2 + a ** 2 * (y - 1) ** 2 - a ** 2 * b ** 2
        while y >= 0: # Рисование нижней части эллипса
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y)]: # симметричные точки эллипса
                self.draw_point(x0 + dx, y0 + dy)
            y -= 1 # Уменьшаем y для перехода к следующей точке
            if d2 > 0: # Если d2 больше 0, x остается прежним, обновляем d2
                d2 += a ** 2 - 2 * a ** 2 * y
            else: # Если d2 меньше или равен 0, увеличиваем x и обновляем d2
                x += 1
                d2 += (2 * b ** 2) * x - (2 * a ** 2) * y + a ** 2

    def draw_hyperbola(self, x0, y0, a, b):
        x, y = a, 0 # x инициализируется радиусом по оси x, y — 0
        # Инициализация d1 для первой части гиперболы
        d1 = b ** 2 * (x + 0.5) ** 2 - a ** 2 * (y + 1) ** 2 - a ** 2 * b ** 2
        while (b ** 2) * (x - 0.5) > (a ** 2) * (y + 1): # Рисование первой ветви гиперболы
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y)]: # Рисуем симметричные точки гиперболы
                self.draw_point(x0 + dx, y0 + dy)

            y += 1  # Увеличиваем y для перехода к следующей точке
            if d1 < 0:  # Если d1 меньше 0, x остается прежним, обновляем d1
                d1 += (2 * a ** 2) * y + a ** 2
            else: # Если d1 больше или равен 0, увеличиваем x и обновляем d1
                x += 1
                d1 += (2 * a ** 2) * y - (2 * b ** 2) * x + a ** 2
        # Инициализация d2 для второй части гиперболы
        d2 = b ** 2 * (x + 1) ** 2 - a ** 2 * (y + 0.5) ** 2 - a ** 2 * b ** 2
        while x < 200: # Рисование второй ветви гиперболы
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y)]: # Рисуем симметричные точки гиперболы
                self.draw_point(x0 + dx, y0 + dy)

            x += 1 # Увеличиваем x для перехода к следующей точке
            if d2 > 0: # Если d2 больше 0, y остается прежним, обновляем d2
                d2 += b ** 2 - (2 * b ** 2) * x
            else: # Если d2 меньше или равен 0, увеличиваем y и обновляем d2
                y += 1
                d2 += (2 * a ** 2) * y - (2 * b ** 2) * x + b ** 2

    def draw_parabola(self, x0, y0, p):
        # Рисует параболу, вычисляя координаты точек.
        step = 1 # величина, на которую увеличивается x в каждой итерации
        x = 0
        while x <= 200: # Цикл для рисования параболы
            y = (x ** 2) / (4 * p) # Вычисление значения y по формуле параболы:
            self.draw_point(x0 + x, y0 - y) # Рисуем точку в правой части параболы
            self.draw_point(x0 - x, y0 - y) # Рисуем симметричную точку в левой части параболы
            x += step # Увеличиваем x на шаг для перехода к следующей точке

    def _setup_ui(self):
        # Установка темной темы
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#23272A")
        style.configure("TLabel", background="#FFFFFF", font=("Arial", 11))
        style.configure("TButton", background="#7289DA", foreground="white", font=("Arial", 10, "bold"), padding=6)
        style.configure("TCombobox", padding=5, font=("Arial", 10))

        # Панель инструментов
        button_panel = ttk.Frame(self, style="TFrame")
        button_panel.pack(side="top", fill="x", padx=10, pady=10)

        self.figure_types = ["Окружность", "Эллипс", "Гипербола", "Парабола"]
        self.figure_selector = ttk.Combobox(button_panel, values=self.figure_types, state="readonly", width=13)
        self.figure_selector.set(self.selected_figure)
        self.figure_selector.pack(side="left", padx=5)
        self.figure_selector.bind("<<ComboboxSelected>>", self._set_figure_type)

        self.clear_button = ttk.Button(button_panel, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side="left", padx=5)

        self.debug_button = ttk.Button(button_panel, text="Отладка", command=self._toggle_debug_mode)
        self.debug_button.pack(side="left", padx=5)

        right_panel = ttk.Frame(button_panel, style="TFrame")
        right_panel.pack(side="left", padx=5)

        self._create_labeled_input(right_panel, "Радиус/a:", 100, "size1_entry")
        self._create_labeled_input(right_panel, "Высота/b:", 50, "size2_entry")

        # Темный холст
        self.canvas = tk.Canvas(self, width=self.draw_area_width, height=self.draw_area_height, bg="#36393F",
                                cursor="crosshair")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Слайдер скорости отладки
        slider_panel = ttk.Frame(self, style="TFrame")
        slider_panel.pack(side="bottom", padx=10, pady=5)

        delay_label = ttk.Label(slider_panel, text="Скорость отладки:", background="#23272A", foreground="white")
        delay_label.pack(side="left", padx=5)

        self.delay_slider = ttk.Scale(slider_panel, from_=1, to=501, orient="horizontal", command=self._update_delay,
                                      length=200)
        self.delay_slider.set(250)
        self.delay_slider.pack(side="left", padx=5)

    def _create_labeled_input(self, parent, label_text, default_value, attribute_name):
        frame = ttk.Frame(parent)
        frame.pack(side="left", padx=5)
        label = ttk.Label(frame, text=label_text)
        label.pack()
        entry = ttk.Entry(frame, width=5)
        entry.insert(0, str(default_value))
        entry.pack()
        setattr(self, attribute_name, entry)

    def _center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coord = (screen_width // 2) - (self.winfo_width() // 2)
        y_coord = (screen_height // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x_coord}+{y_coord}")

    def _draw_grid(self):
        if self.grid_visible:
            for i in range(self.grid_step, self.draw_area_width, self.grid_step):
                self.canvas.create_line(i, 0, i, self.draw_area_height, fill="#44474D", tags="grid_line")
            for i in range(self.grid_step, self.draw_area_height, self.grid_step):
                self.canvas.create_line(0, i, self.draw_area_width, i, fill="#44474D", tags="grid_line")

    def clear_canvas(self):
        self.canvas.delete("all")
        self._draw_grid()

    def _set_figure_type(self, event=None):
        self.selected_figure = self.figure_selector.get()

    def _toggle_debug_mode(self):
        self.is_debugging = not self.is_debugging
        msg = "Режим отладки включен" if self.is_debugging else "Режим отладки выключен"
        messagebox.showinfo("Отладка", msg)

    def _update_delay(self, value):
        self.debug_pause = int(501 - float(value))

    def draw_point(self, x, y):
        self.canvas.create_oval(x, y, x + 2, y + 2, fill=self.selected_color, outline="")
        if self.is_debugging:
            print(f"{self.selected_figure}: (x={x}, y={y})")
        self._pause_if_debugging()

    def _pause_if_debugging(self):
        if self.is_debugging:
            self.update()
            time.sleep(self.debug_pause / 1000)

    def _get_figure_sizes(self):
        try:
            size1 = int(self.size1_entry.get())
            size2 = int(self.size2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные размеры. Используются значения по умолчанию (100, 50).")
            size1, size2 = 100, 50
        return size1, size2

    def _on_canvas_click(self, event):
        if self.is_drawing:
            return
        self.is_drawing = True
        size1, size2 = self._get_figure_sizes()
        if self.selected_figure == "Окружность":
            self.draw_circle(event.x, event.y, size1)
        elif self.selected_figure == "Эллипс":
            self.draw_ellipse(event.x, event.y, size1, size2)
        elif self.selected_figure == "Гипербола":
            self.draw_hyperbola(event.x, event.y, size1, size2)
        elif self.selected_figure == "Парабола":
            self.draw_parabola(event.x, event.y, size1)
        self.is_drawing = False


if __name__ == "__main__":
    app = PaintApp()
    app.mainloop()
