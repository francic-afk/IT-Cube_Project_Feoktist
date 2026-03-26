import tkinter as tk  # Импортируем библиотеку для создания графического интерфейса
from tkinter import messagebox  # Для всплывающих окон
import random  # Для случайной расстановки мин

class Minesweeper:
    def __init__(self, master):
        # Настройки игры
        self.master = master  # Главное окно
        self.master.title("Сапёр - Простая версия")  # Название окна
        self.master.geometry("400x400")  # Размер окна

        # Параметры игры
        self.size = 8  # Размер поля (8x8)
        self.mines = 10  # Количество мин
        self.game_active = True  # Флаг, что игра продолжается

        # Создаем игровое поле
        self.create_buttons()
        self.place_mines()

    def create_buttons(self):
        """Создает кнопки для игрового поля"""
        self.buttons = []  # Список для хранения всех кнопок

        for row in range(self.size):  # Перебираем строки
            row_buttons = []  # Кнопки в одном ряду
            for col in range(self.size):  # Перебираем столбцы
                # Создаем кнопку
                btn = tk.Button(
                    self.master,
                    text="",  # Пустой текст
                    width=2,  # Ширина кнопки
                    height=1,  # Высота кнопки
                    font=("Arial", 12)  # Шрифт
                )
                btn.grid(row=row, column=col)  # Размещаем кнопку в сетке
                # Привязываем левый клик мыши к функции
                btn.bind("<Button-1>", lambda e, r=row, c=col: self.on_left_click(r, c))
                # Привязываем правый клик мыши к функции
                btn.bind("<Button-3>", lambda e, r=row, c=col: self.on_right_click(r, c))
                row_buttons.append(btn)  # Добавляем кнопку в ряд
            self.buttons.append(row_buttons)  # Добавляем ряд в общее поле

    def place_mines(self):
        """Расставляет мины на поле"""
        self.mine_positions = set()  # Множество для хранения позиций мин

        # Пока не расставили нужное количество мин
        while len(self.mine_positions) < self.mines:
            # Выбираем случайные координаты
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            # Добавляем их в множество
            self.mine_positions.add((row, col))

    def on_left_click(self, row, col):
        """Обработка левого клика мыши (открытие клетки)"""
        # Проверяем, что игра не окончена
        if not self.game_active:
            return

        # Если нажали на мину - проигрыш
        if (row, col) in self.mine_positions:
            self.game_over()
            return

        # Открываем клетку
        self.open_cell(row, col)

    def on_right_click(self, row, col):
        """Обработка правого клика мыши (установка флага)"""
        if not self.game_active:
            return

        # Получаем текущий текст кнопки
        current_text = self.buttons[row][col]["text"]

        # Если флага нет, ставим его
        if current_text == "":
            self.buttons[row][col]["text"] = "🚩"
        # Если флаг есть, убираем его
        else:
            self.buttons[row][col]["text"] = ""

    def open_cell(self, row, col):
        """Открывает клетку и показывает, что за ней"""
        # Получаем кнопку
        btn = self.buttons[row][col]

        # Если клетка уже открыта, ничего не делаем
        if btn["state"] == tk.DISABLED:
            return

        # Считаем количество мин вокруг
        mines_around = self.count_mines_around(row, col)

        # Если мины есть - показываем цифру
        if mines_around > 0:
            btn["text"] = str(mines_around)
            btn["state"] = tk.DISABLED  # Делаем кнопку неактивной
            # Красим цифру в зависимости от количества мин
            colors = ["blue", "green", "red", "purple",
                     "maroon", "turquoise", "black", "gray"]
            btn["fg"] = colors[mines_around-1]
        # Если мин нет - открываем пустую клетку
        else:
            btn["text"] = ""
            btn["state"] = tk.DISABLED
            btn["relief"] = tk.SUNKEN  # Делаем кнопку "утопленной"
            # Открываем все соседние клетки
            self.open_around(row, col)

        # Проверяем, выиграл ли игрок
        self.check_win()

    def count_mines_around(self, row, col):
        """Считает количество мин вокруг заданной клетки"""
        count = 0

        # Проверяем все 8 клеток вокруг
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                # Проверяем, что не выходим за границы поля
                if 0 <= r < self.size and 0 <= c < self.size:
                    # Если там мина - увеличиваем счетчик
                    if (r, c) in self.mine_positions:
                        count += 1
        return count

    def open_around(self, row, col):
        """Открывает все клетки вокруг, если они пустые"""
        # Открываем все 8 клеток вокруг
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                # Проверяем, что не выходим за границы поля
                if 0 <= r < self.size and 0 <= c < self.size:
                    # Открываем клетку
                    self.open_cell(r, c)

    def game_over(self):
        """Завершает игру (если игрок нажал на мину)"""
        self.game_active = False

        # Показываем все мины
        for row, col in self.mine_positions:
            btn = self.buttons[row][col]
            # Если мина не помечена флагом, показываем ее
            if btn["text"] != "🚩":
                btn["text"] = "💣"
                btn["bg"] = "red"

        # Показываем сообщение
        messagebox.showinfo("Игра окончена", "Вы проиграли!")

    def check_win(self):
        """Проверяет, выиграл ли игрок"""
        # Считаем количество закрытых клеток
        closed_cells = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.buttons[row][col]["state"] == tk.NORMAL:
                    closed_cells += 1

        # Если все закрытые клетки - это мины, то победа
        if closed_cells == self.mines:
            self.game_active = False
            messagebox.showinfo("Победа", "Вы выиграли!")

# Создаем главное окно и запускаем игру
root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
