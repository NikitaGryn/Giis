# Giis

![image](https://github.com/user-attachments/assets/634a0247-f8b0-4963-8edf-b0cf5678e168)

# Цель: 
Изучить основные виды алгоритмов построения отрезков


# Задача: 
Разработать элементарный графический редактор, реализующий построение отрезков с помощью алгоритма ЦДА, целочисленного алгоритма Брезенхема и алгоритма Ву. Вызов способа генерации отрезка задается из пункта меню и доступно через панель инструментов «Отрезки». В редакторе кроме режима генерации отрезков в пользовательском окне должен быть предусмотрен отладочный режим, где отображается пошаговое решение на дискретной сетке.

# Dda

```python
import time


def draw_line(canvas, x0, y0, x1, y1, debug=False):

    dx = x1 - x0
    dy = y1 - y0

    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        canvas.create_rectangle(round(x0), round(y0), round(x0) + 1, round(y0) + 1, fill="black", outline="black")
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x0, y0

    for i in range(steps + 1):
        canvas.create_rectangle(round(x), round(y), round(x) + 1, round(y) + 1, fill="black", outline="black")

        if debug:
            canvas.update()
            time.sleep(0.05)

        x += x_inc
        y += y_inc

```

# Wu

```python
import math
import time


def _ipart(x):
    return math.floor(x)


def _round(x):
    return _ipart(x + 0.5)


def _fpart(x):
    return x - math.floor(x)


def _rfpart(x):
    return 1 - _fpart(x)


def _plot(canvas, x, y, intensity, debug=False):
    intensity = max(0, min(1, intensity))
    gray_value = int((1 - intensity) * 255)
    color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
    canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)

    if debug:
        canvas.update()
        time.sleep(0.05)


def draw_line(canvas, x0, y0, x1, y1, debug=False):
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1.0

    xend = _round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = _rfpart(x0 + 0.5)
    xpixel1 = xend
    ypixel1 = _ipart(yend)

    if steep:
        _plot(canvas, ypixel1, xpixel1, _rfpart(yend) * xgap, debug)
        _plot(canvas, ypixel1 + 1, xpixel1, _fpart(yend) * xgap, debug)
    else:
        _plot(canvas, xpixel1, ypixel1, _rfpart(yend) * xgap, debug)
        _plot(canvas, xpixel1, ypixel1 + 1, _fpart(yend) * xgap, debug)

    intery = yend + gradient
    xend = _round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = _fpart(x1 + 0.5)
    xpixel2 = xend
    ypixel2 = _ipart(yend)

    if steep:
        _plot(canvas, ypixel2, xpixel2, _rfpart(yend) * xgap, debug)
        _plot(canvas, ypixel2 + 1, xpixel2, _fpart(yend) * xgap, debug)
    else:
        _plot(canvas, xpixel2, ypixel2, _rfpart(yend) * xgap, debug)
        _plot(canvas, xpixel2, ypixel2 + 1, _fpart(yend) * xgap, debug)

    if steep:
        for x in range(xpixel1 + 1, xpixel2):
            y = _ipart(intery)
            _plot(canvas, y, x, _rfpart(intery), debug)
            _plot(canvas, y + 1, x, _fpart(intery), debug)
            intery += gradient
    else:
        for x in range(xpixel1 + 1, xpixel2):
            y = _ipart(intery)
            _plot(canvas, x, y, _rfpart(intery), debug)
            _plot(canvas, x, y + 1, _fpart(intery), debug)
            intery += gradient
```

# Bresenham

```python
import time


def draw_line(canvas, x0, y0, x1, y1, debug=False):

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while True:
        canvas.create_rectangle(x0, y0, x0 + 1, y0 + 1, fill="black", outline="black")

        if debug:
            canvas.update()
            time.sleep(0.05)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy
```

![image](https://github.com/user-attachments/assets/8d0228fd-07cb-41ee-99cb-281bfc1d3733)

# Окружность

```python
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
```

# Элипс

```python
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
```
# Гипербола

```python
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

```


# Парабола

```python

    def draw_parabola(self, x0, y0, p):
        # Рисует параболу, вычисляя координаты точек.
        step = 1 # величина, на которую увеличивается x в каждой итерации
        x = 0
        while x <= 200: # Цикл для рисования параболы
            y = (x ** 2) / (4 * p) # Вычисление значения y по формуле параболы:
            self.draw_point(x0 + x, y0 - y) # Рисуем точку в правой части параболы
            self.draw_point(x0 - x, y0 - y) # Рисуем симметричную точку в левой части параболы
            x += step # Увеличиваем x на шаг для перехода к следующей точке
```


![image](https://github.com/user-attachments/assets/46429670-ce72-4e06-90b8-78e0cf3d043e)

![image](https://github.com/user-attachments/assets/369ddbb6-8aa9-4b9c-894f-647946092561)

![image](https://github.com/user-attachments/assets/ebb93bc4-900c-44f6-839a-7d958000ab6f)


# hermite

```python
    def draw_hermite_curve(self):
        if len(self.points) < 4: # # Проверяем, достаточно ли точек для построения кривой
            return
        # Получаем координаты последних четырех точек
        p0 = [self.points[-4].x, self.points[-4].y] # 1
        p1 = [self.points[-3].x, self.points[-3].y] # 2
        r0 = [self.points[-2].x - p0[0], self.points[-2].y - p0[1]] # Вектор касательной для первой точки
        r1 = [self.points[-1].x - p1[0], self.points[-1].y - p1[1]] # Вектор касательной для 2 точки
        # Генерируем 100 равномерно распределенных значений t от 0 до 1
        t = my_linspace(0, 1, 100)

        # Матрица Эрмита, описывающая формулу для вычисления кривой
        m_hermite = create_matrix(4, 4, [
            2, -2, 1, 1,
            -3, 3, -2, -1,
            0, 0, 1, 0,
            1, 0, 0, 0
        ])

        # Формирование матрицы параметров t
        t_vector_data = [[pow(val, 3), pow(val, 2), val, 1] for val in t]

        # Вычисляем значения x и y для кривой Эрмита
        hermite_x = matrix_mult(m_hermite, create_matrix(4, 1, [p0[0], p1[0], r0[0], r1[0]]))
        hermite_y = matrix_mult(m_hermite, create_matrix(4, 1, [p0[1], p1[1], r0[1], r1[1]]))
        # Вычисляем координаты кривой по каждому значению t
        curve_x = [sum(ti[j] * hermite_x[j][0] for j in range(4)) for ti in t_vector_data]
        curve_y = [sum(ti[j] * hermite_y[j][0] for j in range(4)) for ti in t_vector_data]

        # Рисование кривой
        for i in range(len(curve_x) - 1):
            x1, y1 = curve_x[i], curve_y[i] # Начальные координаты
            x2, y2 = curve_x[i + 1], curve_y[i + 1] # Конечные координаты
            line = self.canvas.create_line(x1, y1, x2, y2, fill="orange")   # Рисуем линию между точками
            self.curve_lines.append(line)
```

# bezier

```python

    def draw_bezier_curve(self):
        if len(self.points) < 4:
            return

        p0 = [self.points[-4].x, self.points[-4].y]
        p3 = [self.points[-3].x, self.points[-3].y]
        p1 = [self.points[-2].x, self.points[-2].y]
        p2 = [self.points[-1].x, self.points[-1].y]

        t = my_linspace(0, 1, 100)

        m_bezier = create_matrix(4, 4, [
            -1, 3, -3, 1,
            3, -6, 3, 0,
            -3, 3, 0, 0,
            1, 0, 0, 0
        ])

        t_vector_data = [[pow(val, 3), pow(val, 2), val, 1] for val in t]

        bezier_x = matrix_mult(m_bezier, create_matrix(4, 1, [p0[0], p1[0], p2[0], p3[0]]))
        bezier_y = matrix_mult(m_bezier, create_matrix(4, 1, [p0[1], p1[1], p2[1], p3[1]]))

        curve_x = [sum(ti[j] * bezier_x[j][0] for j in range(4)) for ti in t_vector_data]
        curve_y = [sum(ti[j] * bezier_y[j][0] for j in range(4)) for ti in t_vector_data]

        for i in range(len(curve_x) - 1):
            x1, y1 = curve_x[i], curve_y[i]
            x2, y2 = curve_x[i + 1], curve_y[i + 1]
            line = self.canvas.create_line(x1, y1, x2, y2, fill="purple")  # Изменен цвет на фиолетовый
            self.curve_lines.append(line)
```
# bspline

```python

    def draw_bspline_curve(self):
        if len(self.points) < 2:
            return

        points = [[point.x, point.y] for point in self.points]
        n = len(points) - 1

        if len(points) >= 3:
            extended_points = points + [points[0], points[1], points[2]]
        else:
            extended_points = points

        all_curve_segments = []
        for i in range(len(extended_points) - 3):
            p0 = extended_points[i]
            p1 = extended_points[i + 1]
            p2 = extended_points[i + 2]
            p3 = extended_points[i + 3]

            t = my_linspace(0, 1, 100)

            m_bspline = create_matrix(4, 4, [
                -1 / 6, 3 / 6, -3 / 6, 1 / 6,
                3 / 6, -6 / 6, 3 / 6, 0,
                -3 / 6, 0, 3 / 6, 0,
                1 / 6, 4 / 6, 1 / 6, 0
            ])

            t_vector_data = [[pow(val, 3), pow(val, 2), val, 1] for val in t]

            bspline_x = matrix_mult(m_bspline, create_matrix(4, 1, [p0[0], p1[0], p2[0], p3[0]]))
            bspline_y = matrix_mult(m_bspline, create_matrix(4, 1, [p0[1], p1[1], p2[1], p3[1]]))

            curve_x = [sum(ti[j] * bspline_x[j][0] for j in range(4)) for ti in t_vector_data]
            curve_y = [sum(ti[j] * bspline_y[j][0] for j in range(4)) for ti in t_vector_data]

            all_curve_segments.append(list(zip(curve_x, curve_y)))

        for curve in all_curve_segments:
            for i in range(len(curve) - 1):
                x1, y1 = curve[i][0], curve[i][1]
                x2, y2 = curve[i + 1][0], curve[i + 1][1]
                line = self.canvas.create_line(x1, y1, x2, y2, fill="cyan")  # Изменен цвет на циановый
                self.curve_lines.append(line)
```

# 3D

![image](https://github.com/user-attachments/assets/37914bf4-2947-490a-ae41-c9c1e0d8a108)


![image](https://github.com/user-attachments/assets/635e17d2-246c-4bb8-9dad-bed634ed6896)

Используемые технологии:

OpenGL: Для отрисовки 3D-объектов и применения матричных преобразований.
Pygame: Для создания окна и управления событиями.
Tkinter: Для создания графического интерфейса с кнопками и диалогами.
Краткое описание работы программы:

Загрузка 3D-объекта: Программа позволяет загружать 3D-объекты из текстовых файлов в формате .txt. Файл содержит вершины (координаты) и грани (связи между вершинами). Вершины представляют собой трехмерные точки, а грани — индексы этих точек, соединенных между собой.

Интерфейс пользователя: Для загрузки 3D-объектов используется графический интерфейс с кнопкой "Открыть файл". Пользователь выбирает файл через стандартный диалог выбора файлов. После загрузки объекта, программа открывает окно с визуализацией 3D-объекта.

Преобразования объекта: Пользователь может применять несколько видов трансформаций:

Поворот объекта вокруг осей X, Y и Z, с помощью клавиш W, S, A, D, Z и X.
Масштабирование объекта, увеличение и уменьшение размера с помощью клавиш Q и E.
Зеркалирование объекта относительно осей X, Y и Z, с помощью клавиш 1, 2 и 3.
Отображение в OpenGL: Все преобразования отображаются в реальном времени. Программа использует OpenGL для отрисовки объекта, где применяется матричная перспектива и преобразования, чтобы объект отображался корректно с учетом различных трансформаций.

Алгоритм работы программы:

Выбор и загрузка файла: Программа запускается с графическим интерфейсом. При нажатии на кнопку "Открыть файл" открывается диалог выбора файла, из которого считываются вершины и грани.

Отображение объекта: Загруженные вершины и грани передаются в OpenGL, где они отображаются как линии, соединяющие вершины в соответствии с гранями объекта.

Обработка событий: Программа отслеживает события от клавиш для применения различных трансформаций:

Для поворота объекта вычисляется угол поворота на основе времени.
Масштабирование изменяет размер объекта, увеличивая или уменьшая его в 1.1 или 0.9 раза.
Зеркалирование применяется через матрицы отражения, изменяя объект относительно выбранной оси.
Применение матричных преобразований: Все трансформации (поворот, масштабирование, зеркалирование) осуществляются с помощью матриц, которые комбинируются и применяются к вершинам объекта.

Рендеринг: После применения всех трансформаций, объект отрисовывается в OpenGL, и программа обновляет окно, отображая измененный объект.


# Polygon

Алгоритм Грэхема

```python

def convex_hull_graham(self):
    if len(self.points) < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек для построения выпуклой оболочки")
        return
    
    points = sorted(self.points, key=lambda p: (p[0], p[1]))  # Сортируем точки по x и y

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])  # Векторное произведение

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()  # Убираем точки, которые образуют "угол" с обратным знаком
        lower.append(p)
    
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]  # Убираем последнюю точку в каждой оболочке, так как она повторяется
    self.draw_polygon(hull, "blue")

```

Проверка на достаточность точек: Если точек меньше 3, то мы не можем построить выпуклую оболочку, так как для этого минимум нужно 3 точки. В этом случае выводим ошибку.

Сортировка точек: Мы начинаем с сортировки всех точек по координате x. Если точки имеют одинаковое значение x, тогда сортируем их по y. Это нужно, чтобы начать строить оболочку с самой левой точки.

Кросс-продукт: Мы используем кросс-продукт для того, чтобы понять, образуют ли три точки правый или левый поворот. Если поворот правый (или коллинеарный), то эта точка не должна быть частью выпуклой оболочки и удаляется.

Строим нижнюю оболочку: Начинаем строить оболочку с левых точек. Если очередная точка формирует правый поворот или лежит на прямой, её убираем, так как она не будет частью оболочки.

Строим верхнюю оболочку: Для верхней оболочки начинаем с правых точек (в обратном порядке). Применяем тот же принцип, что и для нижней оболочки — удаляем точки, которые образуют правый поворот.

Объединение: После того, как мы построили верхнюю и нижнюю оболочку, объединяем их. Важно помнить, что первые и последние точки каждой из оболочек совпадают, поэтому их нужно удалить, чтобы не дублировать.


Алгоритм Джарвиса 

```python

def convex_hull_jarvis(self):
    if len(self.points) < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек для построения выпуклой оболочки")
        return

    def orientation(p, q, r):
        return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])  # Векторное произведение для ориентации

    hull = []
    leftmost = min(self.points, key=lambda p: p[0])  # Самая левая точка
    p = leftmost
    while True:
        hull.append(p)
        q = self.points[0]
        for r in self.points:
            if q == p or orientation(p, q, r) < 0:  # Если точка r находится слева от pq, выбираем ее
                q = r
        p = q
        if p == leftmost:  # Если мы вернулись к начальной точке, то оболочка найдена
            break

    self.draw_polygon(hull, "red")

```

Проверка на достаточность точек: Алгоритм требует минимум 3 точки для построения выпуклой оболочки. Если точек меньше, выводим ошибку.

Функция orientation: Эта функция используется для вычисления ориентации трех точек. Она возвращает:

положительное значение, если поворот между точками против часовой стрелки,
отрицательное значение, если по часовой стрелке,
ноль, если точки коллинеарны (лежат на одной прямой).
Нахождение самой левой точки: Начинаем построение выпуклой оболочки с самой левой точки (точки с минимальной координатой x). Это будет точка, с которой начнется наш обход.

Обход по границе (по часовой стрелке): Мы начинаем с самой левой точки и находим точку, которая является самой левой относительно текущей точки. Для этого мы проверяем все остальные точки на предмет того, какая из них образует самый левый поворот. Эта точка и будет следующей на нашей оболочке.

Переход к следующей точке: После нахождения точки с самым левым поворотом, она становится нашей текущей точкой p. Мы продолжаем искать следующую точку оболочки, пока не вернемся к начальной точке (самой левой). Когда это происходит, мы завершаем построение оболочки.



Алгоритм заливки с использованием AEL

```python

def fill_polygon_ael(self):
    if len(self.points) < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек для полигона")
        return

    # Создаем таблицу ребер (ET)
    et = {}
    for i in range(len(self.points)):
        p1 = self.points[i]
        p2 = self.points[(i + 1) % len(self.points)]

        if p1[1] == p2[1]:
            continue  # Пропускаем горизонтальные ребра

        # Упорядочиваем точки по Y
        if p1[1] > p2[1]:
            p1, p2 = p2, p1

        y_min = int(p1[1])
        y_max = int(p2[1])
        x = p1[0]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        slope = dx / dy  # Δx/Δy

        if y_min not in et:
            et[y_min] = []
        et[y_min].append({'y_max': y_max, 'x': x, 'slope': slope})

    if not et:
        return

    # Инициализация активного списка ребер (AEL)
    ael = []
    current_y = min(et.keys())

    while True:
        # Добавляем новые ребра в AEL
        if current_y in et:
            for edge in et[current_y]:
                ael.append(edge)
            del et[current_y]

        # Сортируем AEL по x
        ael.sort(key=lambda e: e['x'])

        # Закрашиваем горизонтальные отрезки
        i = 0
        while i < len(ael):
            e1 = ael[i]
            if i + 1 >= len(ael):
                break
            e2 = ael[i + 1]

            # Рисуем линию между e1.x и e2.x
            x_start = int(e1['x'])
            x_end = int(e2['x'])

            if x_start > x_end:
                x_start, x_end = x_end, x_start

            self.canvas.create_line(x_start, current_y, x_end, current_y, fill="black")
            i += 2

        # Увеличиваем Y и обновляем AEL
        current_y += 1

        # Удаляем завершенные ребра
        ael = [e for e in ael if e['y_max'] > current_y]

        # Обновляем координаты X для оставшихся ребер
        for edge in ael:
            edge['x'] += edge['slope']

        # Проверяем завершение
        if not ael and not et:
            break


```


построчное заполнение

```python

def start_scanline_fill(self):
    """Запуск построчного заполнения"""
    if len(self.points) < 3:
        messagebox.showerror("Ошибка", "Сначала постройте полигон")
        return

    if self.debug_mode:
        self.prepare_fill_debug('Scanline')
        self.step_fill()
    else:
        def on_click(event):
            x, y = event.x, event.y
            if not self.is_point_inside(x, y):
                messagebox.showerror("Ошибка", "Точка должна быть внутри полигона")
            else:
                self.scanline_fill(x, y)
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.add_point)

        self.canvas.bind("<Button-1>", on_click)
        messagebox.showinfo("Инструкция", "Кликните внутри полигона для выбора точки затравки")

```

Алгоритм заливки с затравкой 

```python

def scanline_fill(self, x, y):
    """Алгоритм заливки с затравкой"""
    # Псевдокод для выполнения заливки
    visited = set()
    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) not in visited and self.is_point_inside(cx, cy):
            visited.add((cx, cy))
            self.canvas.create_line(cx, cy, fill="blue")
            
            # Добавляем соседей (вверх, вниз, влево, вправо)
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

```

ET

```python

def fill_polygon_et(self):
    if len(self.points) < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек для полигона")
        return

    if self.debug_mode:
        self.prepare_fill_debug('ET')
        self._step_et_fill()
    else:
        # Шаг 1: Создаем таблицу ребер (Edge Table)
        et = {}

        # Заполняем таблицу ребер (Edge Table)
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]  # Следующая точка (цикл)

            # Пропускаем горизонтальные ребра
            if p1[1] == p2[1]:
                continue

            # Упорядочиваем точки по Y (по возрастанию)
            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            y_min = int(p1[1])
            y_max = int(p2[1])
            x = p1[0]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            slope = dx / dy  # Наклон ребра

            if y_min not in et:
                et[y_min] = []
            et[y_min].append({'y_max': y_max, 'x': x, 'slope': slope})

        if not et:
            return

        # Шаг 2: Инициализируем активный список ребер (AEL)
        ael = []
        current_y = min(et.keys())

        # Шаг 3: Обрабатываем каждый уровень Y
        while True:
            # Шаг 3a: Добавляем новые ребра в AEL
            if current_y in et:
                for edge in et[current_y]:
                    ael.append(edge)
                del et[current_y]  # Удаляем обработанные ребра

            # Шаг 3b: Сортируем AEL по X-координате
            ael.sort(key=lambda e: e['x'])

            # Шаг 3c: Закрашиваем горизонтальные отрезки между парами ребер
            i = 0
            while i < len(ael):
                if i + 1 >= len(ael):
                    break
                e1 = ael[i]
                e2 = ael[i + 1]

                # Рисуем линию между точками e1.x и e2.x на текущем уровне y
                x_start = int(e1['x'])
                x_end = int(e2['x'])

                if x_start < x_end:
                    self.canvas.create_line(x_start, current_y, x_end, current_y, fill="black")

                i += 2  # Переходим к следующей паре

            # Шаг 3d: Переходим к следующему уровню Y
            current_y += 1

            # Шаг 3e: Удаляем завершенные ребра из AEL и обновляем их X-координаты
            new_ael = []
            for edge in ael:
                if edge['y_max'] > current_y:
                    edge['x'] += edge['slope']  # Обновляем X для активных ребер
                    new_ael.append(edge)
            ael = new_ael

            # Шаг 4: Проверяем завершение работы
            if not ael and not et:
                break


```

1. Алгоритм заливки с затравкой (Seed Fill)
Этот алгоритм заливает область, начиная с заданной точки (затравки) и расширяя заливку на все соседние пиксели, которые удовлетворяют определённым условиям (например, цвет соседей совпадает с цветом затравки). Он используется для заливки замкнутых областей на изображениях.

Принцип работы:

Алгоритм начинает с пикселя, который является точкой входа (затравкой).
Далее проверяются все соседние пиксели (по вертикали, горизонтали или диагонали).
Если соседний пиксель удовлетворяет условиям (например, это часть того же цвета или области), то он также закрашивается, и процесс повторяется для этого пикселя.
Процесс продолжается до тех пор, пока не будут исследованы все возможные соседние пиксели.


2. Алгоритм AEL (Active Edge List)
Это более сложный и продвинутый алгоритм заливки, который использует список активных рёбер (Active Edge List) для эффективной обработки многоугольников. Этот метод обычно используется для заливки многоугольников с отверстиями или сложной структурой.

Принцип работы:

Сначала рёбра сортируются по координате y (по высоте), чтобы обрабатывать их сверху вниз.
Затем используется активный список рёбер, который содержит все рёбра, пересекающиеся с текущим уровнем y.
Каждый раз, когда уровень y изменяется, обновляется этот список, добавляются новые рёбра, а старые удаляются.
После обновления списка активных рёбер на каждом уровне выполняется заливка, соединяя рёбра между собой и закрашивая область между ними.
Алгоритм проходит по всем уровням y, от минимального до максимального.

3. Алгоритм заливки по линии (Edge Fill) ET
Алгоритм заливки по линии используется для заполнения многоугольников, когда необходимо учесть только рёбра и границы области, а не все внутренние пиксели. Этот метод эффективен при обработке векторных объектов, таких как многоугольники.

Принцип работы:

Для начала все рёбра многоугольника определяются и сортируются.
Затем на каждом уровне y (по вертикали) анализируются рёбра, которые пересекают этот уровень.
На основе этих пересечений строится линия, которая закрывает область, заполняя её цветом.
Обычно используются алгоритмы, такие как алгоритм сканирующей линии, для нахождения пересечений с линией сканирования и определения, какие участки должны быть закрашены.

4.Алгоритм Построчного заполнения

На каждом уровне y (горизонтальной строке) алгоритм ищет рёбра, которые пересекаются с этой горизонталью.
Для каждого пересечения с рёбром определяется, где начинается и заканчивается участок, который нужно залить.
Алгоритм проходит по всем пересечениям на текущем уровне и закрашивает область между ними.

![image](https://github.com/user-attachments/assets/51b9f279-e3a4-4711-9290-28b4a44bfa94)


![image](https://github.com/user-attachments/assets/47dee0ce-0c64-4de9-9016-528adc99bc53)

7 лабораторная


Триангуляция Делоне (Delaunay Triangulation) — это разбиение множества точек на плоскости на треугольники так, чтобы никакая точка множества не находилась внутри описанной окружности любого из треугольников.

Как строится:

Берётся множество точек.
Соединяются точки так, чтобы получившиеся треугольники удовлетворяли условию Делоне (описанная окружность каждого треугольника не содержит других точек внутри).
Алгоритм итеративно проверяет и улучшает треугольники, перестраивая их при необходимости.

Диаграмма Вороного (Voronoi Diagram) делит плоскость на области, каждая из которых соответствует одной из заданных точек, так что все точки внутри области ближе к своей исходной точке, чем к любой другой.

Как строится:

Исходные точки размечаются на плоскости.
Вокруг каждой точки строится область (ячейка Вороного), которая содержит все точки, ближайшие именно к этой точке.
Границы между областями строятся по серединным перпендикулярам между соседними точками.

![image](https://github.com/user-attachments/assets/54810771-c423-462f-b13d-d888e6e78217)


![image](https://github.com/user-attachments/assets/0d0d760e-f3ec-458d-bebd-2c6be33dbc0a)
