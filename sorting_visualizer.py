import pygame as pg
import random as rnd

pg.init()


# TODO Selection, heap, quick
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


class Visualizer:
    def __init__(self):
        self._SCR_DIMS = 1024, 768
        self._scr = pg.display.set_mode(self._SCR_DIMS)
        pg.display.set_caption('Sorting Visualizer')

        self._running = True

        self._BRD_SIZE = 600, 500
        self._btns = [MyRect(self._SCR_DIMS[0] - 150 - 50, 200, 150, 75, color=(210, 210, 210))]

        self._nums = []

        self._bars = []
        self._bar_width = 0
        self._bar_height_base = 0

        self._sort_ctrls = {'bubble': False,
                            'insertion': False,
                            'merge': False, }

        self._insertion_index = 1

    def _generate_nums(self, n, start, stop):
        self._nums = [rnd.randint(start, stop) for _ in range(n)]
        self._bar_width = self._BRD_SIZE[0] / len(self._nums)
        self._bar_height_base = self._BRD_SIZE[1] / max(self._nums)

    def _update_bars(self):
        x_offset = -100
        self._bars = [MyRect(
            i * self._bar_width + (self._SCR_DIMS[0] - self._BRD_SIZE[0]) / 2 + x_offset,
            (self._SCR_DIMS[1] - self._BRD_SIZE[1]) / 2 + self._BRD_SIZE[1] - self._bar_height_base * num,
            self._bar_width,
            self._bar_height_base * num) for i, num in enumerate(self._nums)]

    def _draw_bars(self):
        for bar in self._bars:
            pg.draw.rect(self._scr, bar.color, bar)

    def _draw_buttons(self):
        for button in self._btns:
            pg.draw.rect(self._scr, button.color, button)

    def _update_screen(self):
        self._scr.fill((255, 255, 255))
        self._draw_bars()
        self._draw_buttons()
        pg.display.flip()

    def _events_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for button in self._btns:
                    if button.collidepoint(pos):
                        self._sort_ctrls = {k: False for k in self._sort_ctrls.keys()}
                        self._generate_nums(200, 1, 100)
                        self._update_bars()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # delay = 1000 / len(bars)
                    # delay = int(delay) if delay >= 1 else 0
                    self._sort_ctrls['bubble'] = not self._sort_ctrls['bubble']
                elif event.key == pg.K_BACKSPACE:
                    if self._sort_ctrls['insertion']:
                        self._sort_ctrls['insertion'] = False
                    else:
                        self._sort_ctrls['insertion'] = True
                        self._insertion_index = 1
                elif event.key == pg.K_RETURN:
                    self._sort_ctrls['merge'] = not self._sort_ctrls['merge']
                    self._merge_sort()

    def _bubble_sort(self):
        changed = False
        for i in range(1, len(self._nums)):
            if self._nums[i] < self._nums[i - 1]:
                self._nums[i], self._nums[i - 1] = self._nums[i - 1], self._nums[i]
                self._update_bars()
                self._bars[i].select()
                self._update_screen()
                changed = True

        return changed

    def _insertion_sort(self):
        j = self._insertion_index - 1
        while j >= 0 and self._nums[j] > self._nums[j + 1]:
            self._nums[j + 1], self._nums[j] = self._nums[j], self._nums[j + 1]
            self._update_bars()
            self._bars[j].select()
            self._update_screen()
            j -= 1

    def _merge_update_screen(self, k):
        self._update_bars()
        self._bars[k - 1].select()
        self._update_screen()

    def _merge(self, left, right, start_l):
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
            self._merge_update_screen(k)

        while i < len(left):
            self._nums[k] = left[i]
            i += 1
            k += 1
            self._merge_update_screen(k)

        while j < len(right):
            self._nums[k] = right[j]
            j += 1
            k += 1
            self._merge_update_screen(k)

    def _merge_sort(self):
        group_size = 2
        loop = True
        while self._sort_ctrls['merge']:
            self._events_handler()
            if group_size > len(self._nums):
                loop = False
            loop_range = len(self._nums) // group_size + bool(len(self._nums) % group_size)
            for i in range(loop_range):
                mid = group_size // 2 + i * group_size
                start_l = i * group_size
                end_r = mid + group_size // 2
                self._merge(self._nums[start_l: mid], self._nums[mid:end_r], start_l)
                self._update_bars()
                self._update_screen()

            if not loop:
                break
            group_size *= 2

    def _selection_sort(self):
        pass

    def main_loop(self):
        self._generate_nums(200, 1, 100)
        self._update_bars()
        while self._running:
            self._events_handler()

            if self._sort_ctrls['bubble']:
                self._sort_ctrls['bubble'] = self._bubble_sort()

            if self._sort_ctrls['insertion'] and self._insertion_index < len(self._nums):
                self._insertion_sort()
                self._insertion_index += 1

            self._update_screen()


if __name__ == '__main__':
    root = Visualizer()
    root.main_loop()
