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
