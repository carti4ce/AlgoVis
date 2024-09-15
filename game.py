import math
import pygame
import random
pygame.init()

class DrawWindow:
    BLACK = 20, 25, 25
    WHITE = 208, 211, 212
    BLUE = 0, 150, 255
    GREEN = 35, 155, 86
    RED = 231, 76, 60
    GREY = 151, 154, 154
    DARK_GREY = 66, 73, 73
    BACKGROUND = BLACK
    SIDE_PADDING = 50
    TOP_PADDING = 100
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    BAR_COLORS = [
        WHITE,
        GREY,
        DARK_GREY
    ]

    def __init__(self, width, height, lst) -> None:
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AlgoVis")
        self.setList(lst)

    def setList(self, lst) -> None:
        self.lst = lst
        self.maxValue = max(lst)
        self.minValue = min(lst)

        self.barWidth = math.floor((self.width - self.SIDE_PADDING) / len(lst))
        self.barHeight = (self.height - self.TOP_PADDING) / (self.maxValue - self.minValue)
        self.start_x = self.SIDE_PADDING // 2



def generateList(n, minVal, maxVal) -> list:
    lst = []
    for i in range(n):
        value = random.randrange(minVal, maxVal)
        lst.append(value)
    return lst


def draw(drawWindow, algoName, ascending) -> None:
    drawWindow.window.fill(drawWindow.BACKGROUND)

    title = drawWindow.FONT.render(f"{algoName} | {'Ascending' if ascending else 'Descending'}", 1, drawWindow.BLUE)
    drawWindow.window.blit(title, (drawWindow.width / 2 - title.get_width() / 2, 5))

    controlString = "R - Reset | SPACE - Sort | A - Ascending | D - Descending | N = " + str(len(drawWindow.lst))
    controls = drawWindow.FONT.render(controlString, 1, drawWindow.WHITE)
    drawWindow.window.blit(controls, (drawWindow.width / 2 - controls.get_width() / 2, 35))

    sorting = drawWindow.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, drawWindow.WHITE)
    drawWindow.window.blit(sorting, (drawWindow.width / 2 - sorting.get_width() / 2, 65))

    drawList(drawWindow)
    pygame.display.update()


def drawList(drawWindow, colorPositions={}, clearBg=False) -> None:

    if clearBg:
        clearRect = (drawWindow.SIDE_PADDING // 2, drawWindow.TOP_PADDING, drawWindow.width - drawWindow.SIDE_PADDING, drawWindow.height - drawWindow.TOP_PADDING)
        pygame.draw.rect(drawWindow.window, drawWindow.BACKGROUND, clearRect)

    for i, val in enumerate(drawWindow.lst):
        x = drawWindow.start_x + i * drawWindow.barWidth
        y = drawWindow.height - (val - drawWindow.minValue) * drawWindow.barHeight

        color = drawWindow.BAR_COLORS[i % 3]

        if i in colorPositions:
            color = colorPositions[i]

        pygame.draw.rect(drawWindow.window, color, (x, y, drawWindow.barWidth, drawWindow.height))

    if clearBg:
        pygame.display.update()


def bubbleSort(drawWindow, ascending=True):
    lst = drawWindow.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                temp = lst[j]
                lst[j] = lst[j + 1]
                lst[j + 1] = temp
                # lst[j], lst[j + i] = lst[j + 1], lst[j]
                drawList(drawWindow, {j: drawWindow.GREEN , j + 1: drawWindow.RED}, True)
                yield True

    return lst

def insertionSort(drawWindow, ascending=True):
    lst = drawWindow.lst
    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascendingSort = i > 0 and lst[i - 1] > current and ascending
            descendingSort = i > 0 and lst[i - 1] < current and not ascending

            if not ascendingSort and not descendingSort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            drawList(drawWindow, {i: drawWindow.GREEN, i - 1: drawWindow.RED}, True)
            yield True



def main() -> None:

    MIN_VAL = 0
    MAX_VAL = 100
    N = 50

    sorting = False
    ascending = True

    sortingAlgorithm = bubbleSort
    sortingAlgorithmName = "Bubble Sort"
    sortingAlgorithmGenerator = None

    running = True
    clock = pygame.time.Clock()
    clockTick = 60

    lst = generateList(N, MIN_VAL, MAX_VAL)
    testList = lst[:]
    testList.sort()
    print(testList)
    drawWindow = DrawWindow(1200, 900, lst)

    while running:
        clock.tick(clockTick)

        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
                print(drawWindow.lst)
        else:
            draw(drawWindow, sortingAlgorithmName, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generateList(N, MIN_VAL, MAX_VAL)
                drawWindow.setList(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithm(drawWindow, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sortingAlgorithm = insertionSort
                sortingAlgorithmName = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sortingAlgorithm = bubbleSort
                sortingAlgorithmName = "Bubble Sort"
            elif event.key == pygame.K_RIGHT and clockTick < 120:
                clockTick = clockTick + 10
            elif event.key == pygame.K_LEFT and clockTick > 30:
                clockTick = clockTick - 10


    pygame.quit()


if __name__ == '__main__':
    main()