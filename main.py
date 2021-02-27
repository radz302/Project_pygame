import os
import random
import sys

import pygame


def load_image1(name):
    fullname = os.path.join('res', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.mixer.init()

apple_sound = pygame.mixer.Sound("res/apple.wav")

collision_sound = pygame.mixer.Sound("res/col.wav")

go_sound = pygame.mixer.Sound("res/gameover.wav")

fon_sound = pygame.mixer.Sound("res/fon.wav")


def papple():
    apple_sound.play()

    pygame.mixer.music.stop()


def game_over():
    go_sound.play()

    pygame.mixer.music.stop()


def fon_sound1():
    fon_sound.play()

    pygame.mixer.music.stop()


def collision():
    collision_sound.play()

    pygame.time.delay(400)

    pygame.mixer.music.stop()


class Snake(pygame.sprite.Sprite):
    # Здесь голова, хвост и остальная часть тела будут

    # представлены в виде координат (y, x)

    class Cell:
        def __init__(self, coordinate, next=None, prev=None):
            self.coordinate = coordinate
            self.next = next
            self.prev = prev

    def __init__(self, box_size, init_len=5):
        if init_len < 2:
            raise Exception(0)
        self.box_size = box_size
        self.food_location = [None, None]
        self.head = self.Cell(coordinate=[0, init_len - 1])

        iter_cell = self.head

        self.tail = None
        for i in range(init_len - 2, -1, -1):
            iter_cell.next = self.Cell(coordinate=[0, i])
            iter_cell.next.prev = iter_cell
            iter_cell = iter_cell.next

        self.tail = iter_cell

        self.is_alive = True

    def __contains__(self, item: list):
        cell = self.head.next
        while cell is not None:
            if item == cell.coordinate:
                return True

            cell = cell.next
        return False

    def pop(self):
        removing_cell = self.tail
        self.tail = self.tail.prev

        self.tail.next = None

        removing_cell.prev = None

        return removing_cell.coordinate

    def prepend(self, coordinate):
        self.head.prev = self.Cell(coordinate)

        self.head.prev.next = self.head

        self.head = self.head.prev

    def get_direction_facing(self):
        snake_coordinate = self.head.coordinate
        snake_neck_coordinate = self.head.next.coordinate

        if snake_coordinate[0] == snake_neck_coordinate[0]:

            # Горизонтальное положение
            if snake_coordinate[1] > snake_neck_coordinate[1]:

                # голова направлена вниз
                return 3
            else:

                # голова направлена вверх
                return 0
        else:

            # Вертикальное положение
            if snake_coordinate[0] > snake_neck_coordinate[0]:

                # голова направлена направо
                return 2
            else:

                # голова направлена налево
                return 1

    def move(self, direction):

        # параметры направления:l, r, u, d

        if direction == 'u':

            next_coordinate = [self.head.coordinate[0], self.head.coordinate[1] - 1]

        elif direction == 'd':

            next_coordinate = [self.head.coordinate[0], self.head.coordinate[1] + 1]

        elif direction == 'l':

            next_coordinate = [self.head.coordinate[0] - 1, self.head.coordinate[1]]

        elif direction == 'r':

            next_coordinate = [self.head.coordinate[0] + 1, self.head.coordinate[1]]

        else:

            raise Exception("Неверное направление")

        if self.head.next.coordinate == next_coordinate:
            print('Нельзя')
            return 0

            # не можешь двигаться назад

        if -1 in next_coordinate or max(next_coordinate) >= self.box_size:
            self.is_alive = False
            collision()
            print("Столкновение со стеной!")
            return -1

            # столкновение со стеной

        if next_coordinate in self:
            self.is_alive = False
            collision()
            print("Столкновение с самим собой")
            return -2

            # столкновение с самим собой

        if next_coordinate != self.food_location:

            self.pop()
        else:
            papple()

            self.food_location[0] = None
            self.food_location[1] = None

        self.prepend(next_coordinate)

    def iter_through_body_cells(self):
        curr_cell = self.head.next

        while curr_cell:
            yield curr_cell.coordinate
            curr_cell = curr_cell.next


class SnakeBoard:
    direc = ['l', 'r', 'u', 'd']
    score = 0

    def __init__(self, board_size, snake_init_len):
        self.snake = Snake(box_size=board_size, init_len=snake_init_len)
        self.siz = board_size

        self.food_coordinate = self.snake.food_location

        self.initialize_food()

    def initialize_food(self):
        self.food_coordinate = self.snake.food_location = [random.randint(0, self.siz - 1),
                                                           random.randint(0, self.siz - 1)]
        check = True
        while check:
            check = False
            for coord in self.snake.iter_through_body_cells():
                if coord[0] == self.food_coordinate[0] and coord[1] == self.food_coordinate[1]:
                    self.food_coordinate = self.snake.food_location = [random.randint(0, self.siz - 1),
                                                                       random.randint(0, self.siz - 1)]

                    check = True

                    break


# Константы
window = 500

wm = (40, 30, 20, 10)

grc = (100, 100, 100)

grs = 20

flc1 = (60, 155, 0)

flc2 = (60, 120, 0)

snakelen = 4

snakec = (64, 128, 255)

snakeh = 'res/snake_head.png'

gameover = 'res/game over.png'

fonr = 'res/fon.jpg'

applr = (255, 0, 0)

apples = grs // 2 - 3
#


angles = {
    1: 0,
    0: 270,
    3: 90,
    2: 180
}

pygame.init()

# Рисование вертикальных линий

screen = pygame.display.set_mode([window, window + 50])

for x in range(window // grs):
    pygame.draw.line(screen, grc, (x * grs, 0), (x * grs, window))

# Обновление изменений на экране

pygame.display.flip()

clock = pygame.time.Clock()

snake_head = pygame.image.load(snakeh)

fon = pygame.image.load(fonr)

picture1 = pygame.transform.scale(fon, (500, 500))

game = pygame.image.load(gameover)

picture = pygame.transform.scale(game, (500, 300))

snake_head = pygame.transform.scale(snake_head, (grs + 10, grs + 10))

screen.fill((0, 0, 0))

pygame.display.set_caption('Змейка')

score_font = pygame.font.SysFont('Comic Sans MS', 30)


# Функции

def draw_snake(snake_board):
    for coord in snake_board.snake.iter_through_body_cells():
        pygame.draw.rect(screen,
                         snakec,
                         [
                             coord[0] * grs,
                             coord[1] * grs,
                             grs,
                             grs
                         ])

    coord = snake_board.snake.head.coordinate

    snake_head_tmp = pygame.transform.rotate(snake_head, angles[snake_board.snake.get_direction_facing()])

    screen.blit(snake_head_tmp, (
        coord[0] * grs - 5,
        coord[1] * grs - 5,
    ))


def draw_food(snake_board):
    if snake_board.food_coordinate[0] is None:
        return False

    pygame.draw.circle(screen,
                       applr,
                       [
                           snake_board.food_coordinate[0] * grs + (grs // 2),
                           snake_board.food_coordinate[1] * grs + (grs // 2)
                       ],
                       apples)


#


def main():
    session_score = 0

    play_button_size = (170, 80)

    screen.fill((0, 0, 0))

    menu_font = pygame.font.SysFont('Comic Sans MS', 50)

    prev_score_font = pygame.font.SysFont('Comic Sans MS', 40)

    def start_screen():
        fon_sound1()

        screen.fill((0, 0, 0))

        screen.blit(picture1, (0, 0))

        pygame.display.flip()

        clock.tick(60)

    def show_menu():
        game_over()

        screen.fill((0, 0, 0))

        menu_play_text = menu_font.render("Играть", True, (255, 255, 255))

        prev_score_text = prev_score_font.render("Счёт: " + str(session_score), False, (255, 255, 255))

        pygame.draw.rect(screen,
                         'red',
                         [
                             150,
                             370,
                             play_button_size[0],
                             play_button_size[1]
                         ])

        screen.blit(prev_score_text, [
            (window / 2) - (play_button_size[0] / 2),
            (window / 2) - (play_button_size[1] / 2) + 100

        ])
        screen.blit(menu_play_text, [
            150,
            370
        ])
        screen.blit(picture, [
            0,
            0
        ])

    start_screen()

    while True:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()

                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = event.pos

                if 150 <= mouse_pos[0] <= 320 and \
                        300 <= mouse_pos[1] <= 440:
                    session_score = mainloop()

                    show_menu()


# Основной цикл

def mainloop():
    current_heading_direction = 'r'

    prev_heading_direction = current_heading_direction

    sb = SnakeBoard(board_size=window // grs, snake_init_len=snakelen)

    while True:
        if not sb.snake.is_alive:
            return sb.score

        if sb.food_coordinate[0] is None:
            sb.initialize_food()

            sb.score += 10

        # Рисование горизонтальных линий сетки

        screen.fill((0, 0, 0))

        for x in range(window // grs):

            for y in range(window // grs):

                if (x + y) % 2:

                    color = flc1
                else:

                    color = flc2

                pygame.draw.rect(screen,
                                 color,
                                 [
                                     x * grs,
                                     y * grs,
                                     grs,
                                     grs
                                 ])

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):

                return sb.score
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    current_heading_direction = 'u'

                elif event.key == pygame.K_DOWN:

                    current_heading_direction = 'd'

                elif event.key == pygame.K_LEFT:

                    current_heading_direction = 'l'

                elif event.key == pygame.K_RIGHT:

                    current_heading_direction = 'r'

        score_board = score_font.render("Счёт: " + str(sb.score), True, (255, 255, 255))

        screen.blit(score_board, (15, window + 15))

        if sb.snake.move(current_heading_direction) == 0:

            # Движение змеи

            current_heading_direction = prev_heading_direction
        else:
            prev_heading_direction = current_heading_direction

        draw_snake(sb)

        draw_food(sb)

        clock.tick(10)

        # Ограничение до 60 кадров в секунду

        pygame.display.flip()

        # Обновление экрана


if __name__ == '__main__':
    main()
