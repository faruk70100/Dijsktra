import math
import time

import pygame

Width = 800
Win = pygame.display.set_mode((Width, Width))
pygame.display.set_caption("Dijkstra algorithm")

# Common colors saved by name
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
White = (255, 255, 255)
Black = (0, 0, 0)
Purple = (128, 0, 128)
Orange = (255, 165, 0)
Grey = (128, 128, 128)
Turquoise = (64, 224, 208)


class Spot:
    # constructer tanımlandı
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = White
        self.neighbors = []
        self.width = width
        self.len = float("inf")
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == Red

    def is_open(self):
        return self.color == Green

    def is_barrier(self):
        return self.color == Black

    def is_start(self):
        return self.color == Orange

    def is_end(self):
        return self.color == Turquoise

    def reset(self):
        self.color = White

    def make_closed(self):
        self.color = Red

    def make_open(self):
        self.color = Green

    def make_barrier(self):
        self.color = Black

    def make_start(self):
        self.color = Orange

    def make_end(self):
        self.color = Turquoise

    def make_path(self):
        self.color = Purple

    def temp_color(self):
        temp = self.color
        self.color = Yellow
        time.sleep(2)
        self.color = temp

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col < self.total_rows - 1 and self.row < self.total_rows - 1:
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # alt kutuya bakıyor
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # üst kutuya bakıyor
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows + 1 and not grid[self.row][self.col + 1].is_barrier():  # sağ kutuya bakıyor
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # sol kutuya bakıyor
                self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def reconstruct_path(start, end, Draw):
    path = [end]
    temp_node = end
    count = 0
    while True:
        current = path[count]
        for min_spot in current.neighbors:
            if min_spot.len < temp_node.len:
                temp_node = min_spot

        if temp_node.len != 0:
            path.append(temp_node)
            count += 1

        elif temp_node.len == 0:
            path.append(temp_node)
            for spot in path:
                spot.make_path()
            return True
def algorithm(Draw, grid, start, end):
    count: int = 0
    open_set = [start]
    start.len = 0
    all_distance = 1
    temp = 0

    while not len(open_set) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set[count]
        if current != start:
            temp = all_distance + current.len

        if current == end:
            end.make_path()
            reconstruct_path(start, end, Draw)
            return True

        for neighbor in current.neighbors:
            if neighbor.len == float("inf"):
                neighbor.len = temp
            elif neighbor.len != float("inf"):
                if temp < neighbor.len:
                    neighbor.len = temp
            if neighbor not in open_set:
                open_set.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        if current != start:
            current.make_closed()

        count += 1
        Draw()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Grey, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Grey, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(White)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    y, x = pos
    gap = width // rows
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            # get_pressed [0] sol mous tıklanmasını belirtir
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    spot.make_start()

                elif not end and spot != start:
                    end = spot
                    spot.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()
            # get_pressed [2] sağ mous tıklanmasını belirtir
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()


main(Win, Width)
