import pygame as pg
import random as rnd

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

        :return: the current color of the rectangle
        """
        return self._color


class Visualizer:
    """
    Class handling the GUI
    """
    def __init__(self):
        # screen settings
        self._SCR_DIMS = 1024, 768
        self._scr = pg.display.set_mode(self._SCR_DIMS)
        pg.display.set_caption('Sorting Visualizer')

        # pygame loop variable
        self._running = True
        self._clock = pg.time.Clock()

        # interface variables
        self._BRD_SIZE = 600, 600
        self._btns = [MyRect(self._SCR_DIMS[0] - 150 - 50, 200, 150, 75, color=(210, 210, 210))]

        # number generation parameters
        self._nums = []
        self._lower = 1  # lower bound for generated values
        self._higher = 600  # higher bound for generated values
        self._number = 600  # the length of the generated array

        # variables for the graphical representation of numbers to sort
        self._bars = []
        self._bar_width = 0
        self._bar_height_base = 0

        # dict of all implemented sorting algorithms
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

    def _generate_nums(self):
        """
        Generates the random numbers array to be sorted
        """
        self._nums = [rnd.randint(self._lower, self._higher) for _ in range(self._number)]
        self._bar_width = round(self._BRD_SIZE[0] / len(self._nums))
        self._bar_height_base = self._BRD_SIZE[1] / max(self._nums)

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
        for button in self._btns:
            pg.draw.rect(self._scr, button.color, button)

    def _update_screen(self):
        """
        Updates the screen to show the drawn elements
        """
        self._scr.fill((255, 255, 255))
        self._draw_bars()
        self._draw_buttons()
        pg.display.flip()

    def _events_handler(self):
        """
        Handles the pygame events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for button in self._btns:
                    if button.collidepoint(pos):
                        self._insertion_index = 1
                        self._sort_ctrls = {k: False for k in self._sort_ctrls.keys()}
                        self._generate_nums()
                        self._update_bars()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self._sort_ctrls['bubble'] = not self._sort_ctrls['bubble']
                elif event.key == pg.K_BACKSPACE:
                    self._sort_ctrls['insertion'] = not self._sort_ctrls['insertion']
                elif event.key == pg.K_RETURN:
                    self._sort_ctrls['merge'] = not self._sort_ctrls['merge']
                elif event.key == pg.K_UP:
                    self._sort_ctrls['selection'] = not self._sort_ctrls['selection']
                elif event.key == pg.K_DOWN:
                    self._sort_ctrls['quick'] = not self._sort_ctrls['quick']
                elif event.key == pg.K_LEFT:
                    self._sort_ctrls['heap'] = not self._sort_ctrls['heap']
                elif event.key == pg.K_RIGHT:
                    self._sort_ctrls['counting'] = not self._sort_ctrls['counting']
                elif event.key == pg.K_BACKSLASH:
                    self._sort_ctrls['radix'] = not self._sort_ctrls['radix']
                elif event.key == pg.K_F1:
                    self._sort_ctrls['shell'] = not self._sort_ctrls['shell']

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
                return

    def _insertion_sort(self):
        """
        Sorts the numbers' array using the insertion sort algorithm
        """
        if not self._insertion_index < len(self._nums):
            self._insertion_index = 1
            self._sort_ctrls['insertion'] = False
            return
        j = self._insertion_index - 1
        while j >= 0 and self._nums[j] > self._nums[j + 1]:
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
            if left[i] < right[j]:
                self._nums[k] = left[i]
                i += 1
                k += 1
            else:
                self._nums[k] = right[j]
                j += 1
                k += 1
            self._sort_update_screen(k)

        while i < len(left):
            self._nums[k] = left[i]
            i += 1
            k += 1
            self._sort_update_screen(k)

        while j < len(right):
            self._nums[k] = right[j]
            j += 1
            k += 1
            self._sort_update_screen(k)

    def _merge_sort(self):
        """
        Sorts the numbers' array using the merge sort algorithm
        """
        group_size = 2
        loop = True
        while True:
            if group_size > len(self._nums):
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
            stack[index] = start
            index += 1
            stack[index] = pivot_index - 1
            index += 1
            stack[index] = pivot_index + 1
            index += 1
            stack[index] = end
            index += 1
        self._sort_ctrls['quick'] = False

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

            self._update_screen()
            self._clock.tick(60)


if __name__ == '__main__':
    root = Visualizer()
    root.main_loop()
