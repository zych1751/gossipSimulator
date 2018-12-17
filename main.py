import tkinter as tk
import random
import itertools

FIELD_LENGTH = 840
INFO_FIELD_LENGTH = 500
MAX_N = 1000

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.infected = False

    def infect(self):
        if self.infected:
            return False

        self.infected = True
        return True


class Field:
    def __init__(self, n, b):
        self.init(n, b)

    def init(self, n, b):
        self.node_list = []
        self.n = n
        self.b = b
        self.infect_count = 1
        self.uninfect_count = n-1
        self.step = 0
        self.infect_pair = []

        # Generate all possible non-repeating numbers
        num_list = list(itertools.combinations(range(20, FIELD_LENGTH - 20), 2))
        random.shuffle(num_list)
        num_list = num_list[:n]

        for xy in num_list:
            if (xy[0] + xy[1]) % 2 == 0:
                self.node_list.append(Node(xy[0], xy[1]))
            else:
                self.node_list.append(Node(xy[1], xy[0]))
        if len(self.node_list) > 0:
            self.node_list[0].infect()

    def process(self):
        self.step += 1
        self.infect_pair = []
        updated_index = []
        for node in self.node_list:
            if not node.infected:
                continue

            selected_index = list(range(self.n))
            random.shuffle(selected_index)
            selected_index = selected_index[:self.b]

            updated_index.extend(selected_index)

            for idx in selected_index:
                selected_node = self.node_list[idx]
                self.infect_pair.append((node, selected_node))

        for i in updated_index:
            if self.node_list[i].infect():
                self.infect_count += 1
                self.uninfect_count -= 1


class UI:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=FIELD_LENGTH, height=FIELD_LENGTH, background='white')
        self.canvas.pack(side=tk.LEFT, padx=50)

        info_frame = tk.Frame(root, width=INFO_FIELD_LENGTH, height=FIELD_LENGTH)

        temp_frame = tk.Frame(info_frame)
        label = tk.Label(temp_frame)
        label.config(text='number of nodes', font=('', 18))
        label.pack(pady=20, anchor='w')
        label = tk.Label(temp_frame)
        label.config(text='n : ', font=('', 18))
        label.pack(side=tk.LEFT)
        self.n_entry = tk.Entry(temp_frame, font=('', 18), width=8)
        self.n_entry.pack(padx=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        label = tk.Label(temp_frame)
        label.config(text='infect num per step', font=('', 18))
        label.pack(pady=20, anchor='w')
        label = tk.Label(temp_frame)
        label.config(text='b : ', font=('', 18))
        label.pack(side=tk.LEFT)
        self.b_entry = tk.Entry(temp_frame, font=('', 18), width=8)
        self.b_entry.pack(padx=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        label = tk.Label(temp_frame)
        label.config(text='number of infected', font=('', 18))
        label.pack(pady=20, anchor='w')
        label = tk.Label(temp_frame)
        label.config(text='x : ', font=('', 18))
        label.pack(side=tk.LEFT)
        self.x_entry = tk.Entry(temp_frame, font=('', 18), width=8)
        self.x_entry.config(state=tk.DISABLED)
        self.x_entry.pack(padx=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        label = tk.Label(temp_frame)
        label.config(text='number of un-infected', font=('', 18))
        label.pack(pady=20, anchor='w')
        label = tk.Label(temp_frame)
        label.config(text='y : ', font=('', 18))
        label.pack(side=tk.LEFT)
        self.y_entry = tk.Entry(temp_frame, font=('', 18), width=8)
        self.y_entry.config(state=tk.DISABLED)
        self.y_entry.pack(padx=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        label = tk.Label(temp_frame)
        label.config(text='step', font=('', 18))
        label.pack(pady=20, anchor='w')
        label = tk.Label(temp_frame)
        label.config(text='s : ', font=('', 18))
        label.pack(side=tk.LEFT)
        self.s_entry = tk.Entry(temp_frame, font=('', 18), width=8)
        self.s_entry.config(state=tk.DISABLED)
        self.s_entry.pack(padx=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        self.error_label = tk.Label(temp_frame)
        self.error_label.config(font=('', 18), fg='red')
        self.error_label.pack(pady=20)
        temp_frame.pack(fill='x', pady=20)

        temp_frame = tk.Frame(info_frame)
        self.reset_button = tk.Button(temp_frame)
        self.reset_button.config(text='reset', font=('', 18), command=self.reset)
        self.reset_button.pack(padx=20, side=tk.LEFT)
        self.next_button = tk.Button(temp_frame)
        self.next_button.config(text='next', font=('', 18), command=self.process)
        self.next_button.pack(padx=20, side=tk.LEFT)
        temp_frame.pack(fill='x', pady=20)

        info_frame.pack()

        self.field = Field(0, 0)

    def reset(self):
        n, b = (0, 0)
        try:
            n = int(self.n_entry.get())
        except ValueError:
            self.error_label.config(text='n must be integer')
            return

        if not (n >= 1 and n <= MAX_N):
            self.error_label.config(text=('1 <= n <= ' + MAX_N))
            return

        try:
            b = int(self.b_entry.get())
        except ValueError:
            self.error_label.config(text='b must be integer')
            return

        if not (b >= 1 and b <= n):
            self.error_label.config(text=('1 <= b <= ' + str(n)))
            return

        self.error_label.config(text='')
        self.field.init(n, b)
        self.draw()
        return

    def process(self):
        if self.field.n == 0:
            return
        self.field.process()
        self.draw()
        return

    def draw(self):
        self.canvas.delete("all")
        for node in self.field.node_list:
            color = ('red' if node.infected else 'black')
            self.canvas.create_oval(node.x-4, node.y-4, node.x+4, node.y+4, fill=color)

        for pair in self.field.infect_pair:
            self.canvas.create_line(pair[0].x, pair[0].y, pair[1].x, pair[1].y)

        self.x_entry.config(state=tk.NORMAL)
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(self.field.infect_count))
        self.x_entry.config(state=tk.DISABLED)
        self.y_entry.config(state=tk.NORMAL)
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(self.field.uninfect_count))
        self.y_entry.config(state=tk.DISABLED)
        self.s_entry.config(state=tk.NORMAL)
        self.s_entry.delete(0, tk.END)
        self.s_entry.insert(0, str(self.field.step))
        self.s_entry.config(state=tk.DISABLED)
        return


root = tk.Tk()
root.resizable(width=False, height=False)
ui = UI(root)
tk.mainloop()
