from tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageTk


class Painter:
    def __init__(self, size_pole=1000, count_bots=100, time_loop=500):
        self.size_pole = size_pole
        self.count_bots = count_bots

        if self.count_bots >= self.size_pole:
            self.size_bots = 1
        else:
            self.size_bots = size_pole // count_bots

        self.time_loop = time_loop

        self.tk = Tk()

        self.img = Image.new('RGB', (size_pole, size_pole), color='white')
        self.img_dr = ImageDraw.ImageDraw(self.img)
        self.img_tk = ImageTk.PhotoImage(self.img)

        self.lb = Label(self.tk, image=self.img_tk)
        self.lb.grid()

        self.id_run_fun = ''

    def render_pole(self, pole: list[list[int], ]) -> None:
        self.img_dr.rectangle((0, 0, self.size_pole, self.size_pole), fill='white')

        for i in range(1, len(pole) - 1):
            for j in range(1, len(pole) - 1):
                if pole[i][j]:
                    position = ((j - 1) * self.size_bots,
                                (i - 1) * self.size_bots,
                                j * self.size_bots,
                                i * self.size_bots)

                    self.img_dr.rectangle(position, fill='black')

        self.img_tk.paste(self.img)

    def starter_fun_in_loop(self, fun):
        self.id_run_fun = self.lb.after(self.time_loop, lambda: self.lb.after_idle(fun))

    def cancel_after(self):
        self.lb.after_cancel(self.id_run_fun)

    def get_par_win(self):
        return self.tk.winfo_rootx(), self.tk.winfo_rooty()

    def run_painter_loop(self):
        self.lb.mainloop()

    def increase_time_loop(self):
        self.time_loop *= 2

    def reduce_time_loop(self):
        if self.time_loop != 1:
            self.time_loop //= 2
