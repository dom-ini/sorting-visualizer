import pygame as pg
import random as rnd
from typing import Union

pg.init()


class MyRect(pg.Rect):
    """
    Custom class for handling pygame Rects
    """
    def __init__(self, left: float, top: float, width: float, height: float, color: tuple = (0, 0, 0),
                 select_color: tuple = (200, 0, 0)):
        """
        :param left: horizontal position of the rectangle
        :param top: vertical position of the rectangle
        :param width: width of the rectangle
        :param height: height of the rectangle
        :param color: color of the rectangle
        :param select_color: color of the rectangle if selected
        """
        super().__init__(left, top, width, height)
        self._color = color
        self._org_color = color
        self._select_color = select_color

    def select(self):
        """
        Sets the current color of the rectangle to the one marked as selection color
        """
        self._color = self._select_color

    def deselect(self):
        """
        Sets the color of the rectangle to the initial one
        """
        self._color = self._org_color

    @property
    def color(self) -> tuple:
        """
        Getter of the current color of the rectangle
        """
        return self._color


class Cycle:
    """
    Class for repeated cycling through the given list or tuple
    """
    def __init__(self, c: Union[list, tuple]):
        """
        :param c: the list or tuple to cycle through
        """
        self._c = c
        self._index = -1

    def __next__(self):
        self._index += 1
        if self._index >= len(self._c):
            self._index = 0
        return self._c[self._index]

    def reset(self):
        """
        Resets the cycling to the first element
        """
        self._index = -1

    @property
    def previous(self):
        """
        Getter for the previous element of the list or tuple
        """
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c) - 1
        return self._c[self._index]


class Button:
    def __init__(self, position: tuple, size: tuple, border: int = 0, color: tuple = (255, 255, 255),
                 image_path: str = None, image_size: tuple = None, font: pg.font.Font = None, text: str = None,
                 center_text: bool = None, clickable: bool = True):
        """
        :param position: the position of the button on the screen (x, y)
        :param size: the size of the button (x, y)
        :param border: the border size of the button
        :param color: the background color of the button (RGB)
        :param image_path: a path to the button's background image
        :param image_size: the size of the button's image
        :param font: the font of the button's text
        :param text: the text that will be displayed on the button
        :param center_text: if the text has to be centered within the button
        :param clickable: if the button is interactive or not
        """
        self._position = tuple(x - border for x in position)
        self._size = tuple(x + border * 2 for x in size)
        self._border = border
        self._font = font
        self._text = text
        self._center_text = center_text
        self._image_path = image_path
        self._image_size = image_size if image_size else size
        if image_path:
            self._image = pg.image.load(image_path)
            self._image = pg.transform.scale(self._image, self._image_size)
        else:
            self._image = None
        self._org_image = self._image
        self._surface = pg.Surface(self._size, flags=pg.SRCALPHA)
        self._color = color
        self._org_color = color
        self._clickable = clickable
        self._draw()

    def _draw(self):
        """
        Draws the button's elements on its surface
        """
        self._surface.fill(self._color)
        self._rect = pg.Rect(self._position, self._size)
        if self._image:
            self._rect = self._image.get_rect(center=tuple(x / 2 for x in self._size)).move(*self._position)
            self._surface.blit(self._image, tuple((x - y) / 2 for x, y in zip(self._size, self._image_size)))
        elif self._text:
            text = self._font.render(self._text, True, (0, 0, 0))
            text_pos = (0, 0)
            if self._center_text:
                text_pos = tuple((x - y) / 2 for x, y in zip(self._size, text.get_size()))
            self._surface.blit(text, text_pos)
        if self._border:
            # left border
            pg.draw.rect(self._surface, (0, 0, 0), pg.Rect((0, 0), (self._border, self._size[1])))
            # right border
            pg.draw.rect(self._surface, (0, 0, 0), pg.Rect((self._size[0] - self._border, 0),
                                                           (self._border, self._size[1])))
            # top border
            pg.draw.rect(self._surface, (0, 0, 0), pg.Rect((0, 0), (self._size[0], self._border)))
            # bottom border
            pg.draw.rect(self._surface, (0, 0, 0), pg.Rect((0, self._size[1] - self._border),
                                                           (self._size[0], self._border)))

    def update_image(self, image_path: str, image_size: tuple = None):
        """
        Updates the current image of the button

        :param image_path: a path to a new image
        :param image_size: the size of the image
        """
        self._image = pg.image.load(image_path)
        self._image_size = image_size if image_size else self._image_size
        self._image = pg.transform.scale(self._image, self._image_size)
        self._draw()

    def update_text(self, text: str):
        """
        Updates the text on the button

        :param text: the new button's text
        """
        self._text = text
        self._draw()

    def update_color(self, color: tuple):
        """
        Updates the background color of the button

        :param color: the new button's background color (RGB)
        """
        self._color = color
        self._draw()

    def blit(self, surface: pg.Surface):
        """
        Blits the button onto the given surface

        :param surface: pygame Surface to blit the button onto
        """
        surface.blit(self._surface, self._position)

    def check_collision(self, pos: tuple) -> bool:
        """
        Checks if the given coordinates are within the button

        :param pos: the coordinates to check
        :return: 1 if the given point is within the button, 0 otherwise
        """
        return self._rect.collidepoint(pos) if self._clickable else 0

    def reset_image(self):
        """
        Reverts the image of the button to the given one on creation
        """
        self._image = self._org_image
        self._draw()

    @property
    def position(self) -> tuple:
        """
        Getter for the position of the button
        """
        return self._position

    @property
    def size(self) -> tuple:
        """
        Getter for the size of the button
        """
        return self._size

    @property
    def clickable(self) -> bool:
        """
        Getter for the information whether the button is clickable or not
        """
        return self._clickable

    @property
    def org_color(self):
        """
        Getter for the color of the button passed on creation
        """
        return self._org_color


class Visualizer:
    """
    Class handling the GUI
    """
    def __init__(self):
        # screen settings
        self._SCR_DIMS = 1024, 768
        self._ICON = pg.image.load('img/icon.png')
        self._scr = pg.display.set_mode(self._SCR_DIMS)
        pg.display.set_caption('Sorting Visualizer')
        pg.display.set_icon(self._ICON)

        # pygame loop variables
        self._running = True
        self._clock = pg.time.Clock()

        # dict for controlling the state of sorting algorithms
        self._sort_ctrls = {'bubble': False,
                            'insertion': False,
                            'merge': False,
                            'selection': False,
                            'quick': False,
                            'heap': False,
                            'counting': False,
                            'radix': False,
                            'shell': False, }

        # variable for the insertion sort, contains the index of number to be checked
        self._insertion_index = 1

        # sorting algorithm choosing variables
        self._sort_names = Cycle(['bubble', 'insertion', 'merge', 'selection', 'quick', 'heap', 'counting', 'radix',
                                  'shell'])
        self._chosen_sort = next(self._sort_names)
        self._sort_states = Cycle(['start', 'stop'])

        # fonts
        self._fnt = pg.font.SysFont('calibri', 30)

        # interface
        self._BRD_SIZE = 600, 600
        btn_size = 150, 75
        btn_offs_x = 75
        btn_spacing_y = 25
        self._generate_btn = Button(
            position=(self._SCR_DIMS[0] - btn_size[0] - btn_offs_x, (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2),
            size=btn_size, color=(255, 255, 255), border=2, font=self._fnt, text='Generate', center_text=True)

        self._sort_name_btn = Button(
            position=(self._SCR_DIMS[0] - btn_size[0] - btn_offs_x,
                      (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2 + btn_size[1] + btn_spacing_y),
            size=btn_size, color=(255, 255, 255), font=self._fnt, text=self._chosen_sort.capitalize(), center_text=True,
            clickable=False)

        self._start_pause_btn = Button(
            position=(self._SCR_DIMS[0] - btn_size[0] - btn_offs_x,
                      (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2 + (btn_size[1] + btn_spacing_y) * 2),
            size=btn_size, color=(255, 255, 255), border=2, font=self._fnt, text=next(self._sort_states).capitalize(),
            center_text=True)

        self._exit_btn = Button(
            position=(self._SCR_DIMS[0] - btn_size[0] - btn_offs_x,
                      (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2 + (btn_size[1] + btn_spacing_y) * 3),
            size=btn_size, color=(255, 255, 255), border=2, font=self._fnt, text='Exit', center_text=True)

        self._text_btns = [self._generate_btn, self._sort_name_btn, self._start_pause_btn, self._exit_btn]

        arrow_btn_size = 50, 50
        arrow_btn_offs_x = 10
        self._arrow_l_btn = Button(
            position=(self._text_btns[1].position[0] - arrow_btn_size[0] - arrow_btn_offs_x,
                      self._text_btns[1].position[1] + (self._text_btns[1].size[1] - arrow_btn_size[1]) / 2),
            size=arrow_btn_size, image_path='img/arrow_l.png')

        self._arrow_r_btn = Button(
            position=(self._text_btns[1].position[0] + self._text_btns[1].size[0] + arrow_btn_offs_x,
                      self._text_btns[1].position[1] + (self._text_btns[1].size[1] - arrow_btn_size[1]) / 2),
            size=arrow_btn_size, image_path='img/arrow_r.png')

        self._arrow_btns = [self._arrow_l_btn, self._arrow_r_btn]

        # number generation parameters
        self._nums = []
        self._lower = 1  # lower bound for generated values
        self._higher = 600  # higher bound for generated values
        self._number = 600  # the length of the generated array
        self._sorted = False

        # variables for the graphical representation of numbers to sort
        self._bars = []
        self._bar_width = 0
        self._bar_height_base = 0

    def _generate_nums(self):
        """
        Generates the random numbers array to be sorted
        """
        self._nums = [rnd.randint(self._lower, self._higher) for _ in range(self._number)]
        self._bar_width = round(self._BRD_SIZE[0] / len(self._nums))
        self._bar_height_base = round(self._BRD_SIZE[1] / max(self._nums))
        self._sorted = False

    def _update_bars(self):
        """
        Update the bars size and position based on the numbers' array
        """
        x_offset = -100
        self._bars = [MyRect(
            i * self._bar_width + (self._SCR_DIMS[0] - self._BRD_SIZE[0]) / 2 + x_offset,
            (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2 + self._BRD_SIZE[1] - self._bar_height_base * num,
            self._bar_width,
            self._bar_height_base * num) for i, num in enumerate(self._nums)]

    def _draw_bars(self):
        """
        Draws the bars on the screen
        """
        for bar in self._bars:
            pg.draw.rect(self._scr, bar.color, bar)

    def _draw_buttons(self):
        """
        Draws the buttons on the screen
        """
        for button in self._text_btns:
            button.blit(self._scr)
        for button in self._arrow_btns:
            button.blit(self._scr)

    def _update_screen(self):
        """
        Updates the screen to show the drawn elements
        """
        self._scr.fill((255, 255, 255))
        self._draw_bars()
        self._draw_buttons()
        pg.display.flip()

    def _button_hover(self, pos: tuple, hover_color: tuple = (210, 210, 210)):
        """
        Creates the hover effect on the buttons within the given list

        :param pos: the mouse position
        :param hover_color: the color of hovered button
        """
        for button in self._text_btns:
            if button.check_collision(pos) and button.clickable:
                button.update_color(color=hover_color)
            else:
                button.update_color(color=button.org_color)
        for button, dir_ in zip(self._arrow_btns, ('l', 'r')):
            if button.check_collision(pos) and button.clickable:
                button.update_image(f'img/arrow_{dir_}_hover.png')
            else:
                button.reset_image()

    def _reset_sort(self):
        self._insertion_index = 1
        self._sort_ctrls = {k: False for k in self._sort_ctrls.keys()}
        self._sort_states.reset()
        self._start_pause_btn.update_text(next(self._sort_states).capitalize())
        self._generate_nums()
        self._update_bars()

    def _events_handler(self):
        """
        Handles the pygame events
        """
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                self._running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self._generate_btn.check_collision(pos):
                    self._reset_sort()
                if self._start_pause_btn.check_collision(pos):
                    self._sort_ctrls[self._chosen_sort] = not self._sort_ctrls[self._chosen_sort]
                    self._start_pause_btn.update_text(next(self._sort_states).capitalize())
                if self._arrow_r_btn.check_collision(pos):
                    self._chosen_sort = next(self._sort_names)
                    self._sort_name_btn.update_text(self._chosen_sort.capitalize())
                    self._reset_sort()
                if self._arrow_l_btn.check_collision(pos):
                    self._chosen_sort = self._sort_names.previous
                    self._sort_name_btn.update_text(self._chosen_sort.capitalize())
                    self._reset_sort()
                if self._exit_btn.check_collision(pos):
                    self._running = False
            self._button_hover(pos)

    def _sort_update_screen(self, i: int):
        """
        Used inside the sorting functions, used to update bars position and size through the algorithm and to indicate,
        which number is being sorted at the moment

        :param i: the index of bar to be marked
        """
        self._update_bars()
        self._bars[i].select()
        self._update_screen()

    def _bubble_sort(self):
        """
        Sorts the numbers' array using the bubble sort algorithm
        """
        while True:
            changed = False
            for i in range(1, len(self._nums)):
                self._events_handler()
                if not self._sort_ctrls['bubble']:
                    return
                if self._nums[i] < self._nums[i - 1]:
                    self._nums[i], self._nums[i - 1] = self._nums[i - 1], self._nums[i]
                    self._sort_update_screen(i)
                    changed = True
            if not changed:
                self._sort_ctrls['bubble'] = False
                self._sorted = True
                return

    def _insertion_sort(self):
        """
        Sorts the numbers' array using the insertion sort algorithm
        """
        if not self._insertion_index < len(self._nums):
            self._insertion_index = 1
            self._sort_ctrls['insertion'] = False
            self._sorted = True
            return
        j = self._insertion_index - 1
        while j >= 0 and self._nums[j] > self._nums[j + 1]:
            self._events_handler()
            self._nums[j + 1], self._nums[j] = self._nums[j], self._nums[j + 1]
            self._sort_update_screen(j)
            j -= 1
        self._insertion_index += 1

    def _merge(self, left: list, right: list, start_l: int):
        """
        Auxiliary function for merge sort algorithm, merges the left and right arrays

        :param left: the left sub-array to merge
        :param right: the right sub-array to merge
        :param start_l: the starting index of left sub-array within the main array
        """
        if not self._sort_ctrls['merge']:
            return
        i = j = 0
        k = start_l

        while i < len(left) and j < len(right):
            self._sort_update_screen(k)
            if left[i] < right[j]:
                self._nums[k] = left[i]
                i += 1
                k += 1
            else:
                self._nums[k] = right[j]
                j += 1
                k += 1

        while i < len(left):
            self._nums[k] = left[i]
            self._sort_update_screen(k)
            i += 1
            k += 1

        while j < len(right):
            self._nums[k] = right[j]
            self._sort_update_screen(k)
            j += 1
            k += 1

    def _merge_sort(self):
        """
        Sorts the numbers' array using the merge sort algorithm
        """
        group_size = 2
        loop = True
        while True:
            if group_size > len(self._nums) or self._sorted:
                loop = False
            loop_range = len(self._nums) // group_size + bool(len(self._nums) % group_size)
            for i in range(loop_range):
                self._events_handler()
                if not self._sort_ctrls['merge']:
                    return
                mid = group_size // 2 + i * group_size
                start_l = i * group_size
                end_r = mid + group_size // 2
                self._merge(self._nums[start_l: mid], self._nums[mid:end_r], start_l)
                self._update_bars()
                self._update_screen()

            if not loop:
                self._sort_ctrls['merge'] = False
                self._sorted = True
                return
            group_size *= 2

    def _selection_sort(self):
        """
        Sorts the numbers' array using the selection sort algorithm
        """
        start = 0
        for j in range(len(self._nums)):
            self._clock.tick(30)
            min_val = None
            min_index = None
            for i in range(start, len(self._nums)):
                if not self._sort_ctrls['selection']:
                    return
                self._events_handler()
                if min_val is None:
                    min_val = self._nums[i]
                    min_index = i
                elif min_val > self._nums[i]:
                    min_val = self._nums[i]
                    min_index = i
            self._nums[start], self._nums[min_index] = self._nums[min_index], self._nums[start]
            start += 1
            self._sort_update_screen(min_index)
        self._sort_ctrls['selection'] = False
        self._sorted = True

    def _partition(self, start: int, end: int):
        """
        Auxiliary function for the quick sort algorithm, moves the elements in the array according to the pivot

        :param start: the first index of sub-array
        :param end: the last index of sub-array
        :return: the correct index of pivot
        """
        pivot = self._nums[end]
        i = start - 1
        for j in range(start, end):
            self._events_handler()
            self._clock.tick(120)
            if not self._sort_ctrls['quick']:
                return
            if self._nums[j] < pivot:
                i += 1
                self._nums[i], self._nums[j] = self._nums[j], self._nums[i]
            self._sort_update_screen(j)
        i += 1
        self._nums[i], self._nums[end] = self._nums[end], self._nums[i]
        return i

    def _quick_sort(self):
        """
        Sorts the numbers' array using the quick sort algorithm
        """
        stack = [0 for _ in range(len(self._nums))]
        start, end, index = 0, len(self._nums) - 1, 0
        stack[index] = start
        index += 1
        stack[index] = end
        index += 1
        while index > 0:
            index -= 1
            end = stack[index]
            index -= 1
            start = stack[index]
            if start >= end:
                continue
            pivot_index = self._partition(start, end)
            if not self._sort_ctrls['quick']:
                return
            elif self._sorted:
                self._sort_ctrls['quick'] = False
                return
            stack[index] = start
            index += 1
            stack[index] = pivot_index - 1
            index += 1
            stack[index] = pivot_index + 1
            index += 1
            stack[index] = end
            index += 1
        self._sort_ctrls['quick'] = False
        self._sorted = True

    def _maxify_heap(self, n, parent_i):
        """
        Auxiliary function for heap sort algorithm, creates the max heap from the array with the given length

        :param n: the length of the array to create max heap from
        :param parent_i: index of parent node
        """
        self._events_handler()
        if not self._sort_ctrls['heap']:
            return
        left = 2 * parent_i + 1
        right = 2 * parent_i + 2
        largest_i = parent_i
        self._sort_update_screen(parent_i)

        if left < n and self._nums[left] > self._nums[largest_i]:
            largest_i = left
        if right < n and self._nums[right] > self._nums[largest_i]:
            largest_i = right

        if largest_i != parent_i:
            self._nums[parent_i], self._nums[largest_i] = self._nums[largest_i], self._nums[parent_i]
            self._maxify_heap(n, largest_i)

    def _heap_sort(self):
        """
        Sorts the numbers' array using the heap sort algorithm
        """
        last_parent_i = len(self._nums) // 2 - 1
        for i in range(last_parent_i, -1, -1):
            self._maxify_heap(len(self._nums), i)
        for j in range(len(self._nums) - 1, 0, -1):
            self._nums[j], self._nums[0] = self._nums[0], self._nums[j]
            self._maxify_heap(j, 0)
        self._sort_ctrls['heap'] = False
        self._sorted = True

    def _counting_sort(self):
        """
        Sorts the numbers' array using the counting sort algorithm
        """
        arr = self._nums[:]
        counter = {i: 0 for i in range(max(arr) + 1)}
        for num in arr:
            counter[num] += 1
        for i in range(1, len(counter)):
            counter[i] += counter[i - 1]
        for num in arr:
            self._events_handler()
            self._clock.tick(20)
            if not self._sort_ctrls['counting']:
                return
            new_index = counter[num] - 1
            counter[num] -= 1
            self._nums[new_index] = num
            self._sort_update_screen(new_index)
        self._sort_ctrls['counting'] = False
        self._sorted = True

    def _radix_sort(self):
        """
        Sorts the numbers' array using the radix sort algorithm
        """
        max_ = max(self._nums)
        exp = 1
        while max_ / exp > 1:
            counter_range = max([i // exp % 10 for i in self._nums])
            counter = {i: 0 for i in range(counter_range + 1)}
            sorted_arr = [None] * len(self._nums)
            for num in self._nums:
                counter[num // exp % 10] += 1
            for i in range(1, len(counter)):
                counter[i] += counter[i - 1]
            for num in self._nums[::-1]:
                new_index = counter[num // exp % 10] - 1
                sorted_arr[new_index] = num
                counter[num // exp % 10] -= 1
            for i, num in enumerate(sorted_arr):
                self._events_handler()
                self._clock.tick(60)
                if not self._sort_ctrls['radix']:
                    return
                self._nums[i] = num
                self._sort_update_screen(i)
            exp *= 10
        self._sort_ctrls['radix'] = False
        self._sorted = True

    def _shell_sort(self):
        """
        Sorts the numbers' array using the shell sort algorithm
        """
        dist = len(self._nums) // 2
        iteration = 1
        while dist > 0:
            for i in range(dist, len(self._nums)):
                j = i
                while j >= dist and self._nums[j - dist] > self._nums[j]:
                    self._events_handler()
                    self._clock.tick(60)
                    if not self._sort_ctrls['shell']:
                        return
                    self._nums[j], self._nums[j - dist] = self._nums[j - dist], self._nums[j]
                    self._sort_update_screen(j)
                    j -= dist
            iteration += 1
            dist //= 2
        self._sort_ctrls['shell'] = False
        self._sorted = True

    def main_loop(self):
        """
        Main program handler
        """
        self._generate_nums()
        self._update_bars()
        while self._running:
            self._events_handler()
            if self._sort_ctrls['bubble']:
                self._bubble_sort()
            if self._sort_ctrls['insertion']:
                self._insertion_sort()
            if self._sort_ctrls['merge']:
                self._merge_sort()
            if self._sort_ctrls['selection']:
                self._selection_sort()
            if self._sort_ctrls['quick']:
                self._quick_sort()
            if self._sort_ctrls['heap']:
                self._heap_sort()
            if self._sort_ctrls['counting']:
                self._counting_sort()
            if self._sort_ctrls['radix']:
                self._radix_sort()
            if self._sort_ctrls['shell']:
                self._shell_sort()
            if self._sorted:
                self._sort_states.reset()
                self._start_pause_btn.update_text(next(self._sort_states).capitalize())
            self._update_screen()
            self._clock.tick(60)


if __name__ == '__main__':
    root = Visualizer()
    root.main_loop()
