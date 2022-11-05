from random import randint

import main

#Класс точка
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass
#Класс корабль
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots
# Класс доска
class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [ ["O"]*size for _ in range(size) ]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)


        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []
# Класс игрок
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)
    def move2(self, board_us):
        while True:
            try:
                target = self.ask(board_us)
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)
# Интилект компьютера
class AI(Player):
    def ask(self, board_us):

        shot=True
        near = [
            (-1, 0),(0, -1), (0, 1),(1, 0)
        ]
        #Добивание раненого коробля
        for ships in board_us.board.ships:
            if ships.l!=ships.lives and ships.lives>0 and shot :
                i=0
                while i<ships.l:
                    if board_us.board.field[ships.dots[i].x][ships.dots[i].y]=="X":
                        d =Dot(ships.dots[i].x,ships.dots[i].y)
                        for dx, dy in near :
                            cur = Dot(d.x + dx, d.y + dy)
                            if not (self.board.out(cur)) and cur not in board_us.board.busy:
                                print(f"Ход компьютера: {cur.x + 1} {cur.y + 1}")
                                shot =False
                                return cur
                                break
                    i +=1

        if shot:
            #Проверка стрельбы по занятым клеткам и поиск больших короблей в первую очередь
            while True:
                d = Dot(randint(0,5), randint(0, 5))
                if d not in board_us.board.busy and board_us.board.ships[0].lives>0 :
                    for dx, dy in near:
                        cur = Dot(d.x + dx, d.y + dy)
                        cur2 =Dot(d.x + dx+dx, d.y + dy+dy)
                        if not (self.board.out(cur)) and cur not in board_us.board.busy and not (self.board.out(cur2)) and cur2 not in board_us.board.busy:
                            print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                            shot = False
                            return d
                            break
                        else:
                            if not (self.board.out(cur)) and cur not in board_us.board.busy and not (
                            self.board.out(cur2)) and cur2 not in board_us.board.busy:
                                print("shot2")
                                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                                shot = False
                                return d
                                break

                else:
                    if d not in board_us.board.busy and (board_us.board.ships[1].lives>0 or board_us.board.ships[2].lives>0) :
                        for dx, dy in near:
                            cur = Dot(d.x + dx, d.y + dy)
                            if not (self.board.out(cur)) and cur not in board_us.board.busy:
                                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                                shot = False
                                return d
                                break
                if d not in board_us.board.busy and board_us.board.ships[0].lives==0 and board_us.board.ships[1].lives==0 and board_us.board.ships[2].lives==0:
                    print(f"Ход компьютера: {d.x+1} {d.y+1}")
                    return d
                    break

# Класс игрок
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)
# Класс игра
class Game:
    def connect_boards(first, second):
        first_lines = first.split("\n")
        second_lines = second.split("\n")
        result = ""
        for i in range(len(first_lines)):
            result_line = f"{first_lines[i]:27}   ||   {second_lines[i]} \n"
            result += result_line
        return result
    def __init__(self, size = 6):
        self.size = size
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)


    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size = self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")


    def loop(self):
        num = 0
        while True:
            print()
            # Прорисовка объеденненых игровых досок
            user_board = "Доска пользователя:\n"+  str(self.us.board)
            ai_board = "Доска компьютера:\n" + str(self.ai.board)
            print(Game.connect_boards(user_board, ai_board))
            print("Количество живых короблей %d   ||  Количество живых короблей %d"%((7-self.us.board.count),(7-self.ai.board.count)))

            if num % 2 == 0:
                print("-"*62)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*62)
                print("Ходит компьютер!")
                repeat = self.ai.move2(self.us)
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-"*62)
                user_board = "Доска пользователя:\n" + str(self.us.board)
                ai_board = "Доска компьютера:\n" + str(self.ai.board)
                print(Game.connect_boards(user_board, ai_board))
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-"*62)
                user_board = "Доска пользователя:\n" + str(self.us.board)
                ai_board = "Доска компьютера:\n" + str(self.ai.board)
                print(Game.connect_boards(user_board, ai_board))
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()