import pygame as pg
from dataclasses import dataclass
import random as rnd


class MyRect(pg.Rect):
    def __init__(self, left, top, width, height, color=(0, 0, 0), select_color=(200, 0, 0)):
        super().__init__(left, top, width, height)
        self._color = color
        self._org_color = color
        self._select_color = select_color
    
    def select(self):
        self._color = self._select_color
    
    def deselect(self):
        self._color = self._org_color

    @property
    def color(self):
        return self._color

def generate_nums(n, start, stop):
    nums = [rnd.randint(start, stop) for _ in range(n)]
    return nums

def update_bars(nums, bars=[], create=False):
    global BOARD_SIZE
    global SCREEN_DIMS
    bar_width = BOARD_SIZE[0] / len(nums)
    bar_height_base = BOARD_SIZE[1] / max(nums)
    x_offset = -100
    if create:
        bars = [MyRect(
            i * bar_width + (SCREEN_DIMS[0] - BOARD_SIZE[0]) / 2 + x_offset, 
            (SCREEN_DIMS[1] - BOARD_SIZE[1]) / 2 + BOARD_SIZE[1] - bar_height_base * num, 
            bar_width, 
            bar_height_base * num
            ) for i, num in enumerate(nums)]
    else:
        for bar, num in zip(bars, enumerate(nums)):
            i, num = num
            bars[i] = MyRect(
                i * bar_width + (SCREEN_DIMS[0] - BOARD_SIZE[0]) / 2 + x_offset, 
                (SCREEN_DIMS[1] - BOARD_SIZE[1]) / 2 + BOARD_SIZE[1] - bar_height_base * num, 
                bar_width, 
                bar_height_base * num)
    return bars

def draw_bars(bars):
    global SCREEN
    for bar in bars:
        pg.draw.rect(SCREEN, bar.color, bar)

def update_ui(bars):
    global SCREEN
    SCREEN.fill((255, 255, 255))
    draw_bars(bars)
    draw_buttons()
    pg.display.flip()

def bubble_sort(nums, bars):
    changed = False
    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            nums[i], nums[i - 1] = nums[i - 1], nums[i]
            bars = update_bars(nums, bars)
            bars[i - 1].select()
            update_ui(bars)
            changed = True

    return nums, bars, changed

def insertion_sort(nums, bars, i):
    j = i - 1
    while j >= 0 and nums[j] > nums[j + 1]:
        nums[j + 1], nums[j] = nums[j], nums[j + 1]
        bars = update_bars(nums, bars)
        bars[i].select()
        update_ui(bars)
        j -= 1

    return nums, bars    

def draw_buttons():
    global SCREEN
    global BUTTONS
    for button in BUTTONS:
        pg.draw.rect(SCREEN, (210, 210, 210), button)
    

def main():
    global SCREEN
    global BUTTONS
    bubble_running = False
    insertion_running = False
    running = True
    nums = generate_nums(150, 1, 100)
    bars = update_bars(nums, create=True)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for button in BUTTONS:
                    if button.collidepoint(pos):
                        bubble_running = False
                        insertion_running = False
                        nums = generate_nums(200, 1, 100)
                        bars = update_bars(nums, create=True)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    delay = 1000 / len(bars)
                    delay = int(delay) if delay >= 1 else 0
                    bubble_running = not bubble_running
                elif event.key == pg.K_BACKSPACE:
                    if insertion_running:
                        insertion_running = False
                    else:
                        insertion_running = True
                        insertion_index = 1

        SCREEN.fill((255, 255, 255))

        if bubble_running:
            nums, bars, bubble_running = bubble_sort(nums, bars)
        
        if insertion_running and insertion_index < len(nums):
            nums, bars = insertion_sort(nums, bars, insertion_index)
            insertion_index += 1
        
        draw_buttons()
        draw_bars(bars)
        pg.display.flip()
        

if __name__ == '__main__':
    pg.init()
    SCREEN_DIMS = 1024, 768
    BOARD_SIZE = 600, 500
    SCREEN = pg.display.set_mode(SCREEN_DIMS)
    BUTTONS = [
        pg.Rect(
            SCREEN_DIMS[0] - 150 - 50,
            200,
            150,
            75
        )
    ]

    main()