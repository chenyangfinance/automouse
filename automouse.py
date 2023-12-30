import tkinter as tk
from tkinter import ttk, messagebox, font
import pyautogui
import time
import threading

class MouseAutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mouse Automation")

        self.create_widgets()
        self.set_initial_window_size()


    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.mouse_position_frame = ttk.Frame(self.main_frame, relief=tk.GROOVE, borderwidth=2)
        self.mouse_position_frame.grid(row=0, column=0, padx=20, pady=20, sticky=tk.NSEW)

        self.mouse_move_frame = ttk.Frame(self.main_frame, relief=tk.GROOVE, borderwidth=2)
        self.mouse_move_frame.grid(row=0, column=1, padx=20, pady=20, sticky=tk.NSEW)

        self.create_mouse_position_widgets()
        self.create_mouse_move_widgets()

        bold_font = font.Font(weight="bold", size = 12)
        self.position_function_label.config(font=bold_font)
        self.move_function_label.config(font=bold_font)

        # Add a note at the bottom
        self.note_label = ttk.Label(self.main_frame, text="Code by @Chen Yang in Dec 2023")
        self.note_label.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.S)  # Change this line
        
    def set_initial_window_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if screen_width > screen_height:
            # Landscape orientation
            width_ratio = 0.45
            height_ratio = 0.55
        else:
            # Portrait orientation
            width_ratio = 0.55
            height_ratio = 0.45

        width = int(screen_width * width_ratio)
        height = int(screen_height * height_ratio)

        self.geometry(f"{width}x{height}")
        self.minsize(width, height)

    def create_mouse_position_widgets(self):
        self.position_function_label = ttk.Label(self.mouse_position_frame, text="Record Mouse Position")
        self.position_function_label.grid(row=0, column=0, pady=10)

        self.position_label = ttk.Label(self.mouse_position_frame, text="X: 0 Y: 0")
        self.position_label.grid(row=1, column=0, pady=20)

        self.start_position_btn = ttk.Button(self.mouse_position_frame, text="Start", command=self.start_position_thread)
        self.start_position_btn.grid(row=2, column=0, pady=10)

        self.stop_position_btn = ttk.Button(self.mouse_position_frame, text="Stop", command=self.stop_position_thread, state=tk.DISABLED)
        self.stop_position_btn.grid(row=3, column=0, pady=10)

        self.position_thread_running = False

        self.recorded_positions_label = ttk.Label(self.mouse_position_frame, text="Press ENTER to Record Positions:")
        self.recorded_positions_label.grid(row=4, column=0, pady=10)

        self.recorded_positions_text = tk.Text(self.mouse_position_frame, width=20, height=10, state=tk.DISABLED)
        self.recorded_positions_text.grid(row=5, column=0)

        self.recorded_positions_clear_btn = ttk.Button(self.mouse_position_frame, text="Clear", command=self.clear_recorded_positions, state=tk.DISABLED)
        self.recorded_positions_clear_btn.grid(row=6, column=0, pady=10)

        self.bind("<Return>", self.record_position)

    def clear_recorded_positions(self):
        self.recorded_positions_text.config(state=tk.NORMAL)
        self.recorded_positions_text.delete(1.0, tk.END)
        self.recorded_positions_text.config(state=tk.DISABLED)

    def record_position(self, event):
        if self.position_thread_running:
            x, y = pyautogui.position()
            position_str = f"X: {x} Y: {y}\n"
            self.recorded_positions_text.config(state=tk.NORMAL)
            self.recorded_positions_text.insert(tk.END, position_str)
            self.recorded_positions_text.config(state=tk.DISABLED)

    def start_position_thread(self):
        if not self.position_thread_running:
            self.position_thread_running = True
            self.start_position_btn.config(state=tk.DISABLED)
            self.stop_position_btn.config(state=tk.NORMAL)
            self.recorded_positions_text.config(state=tk.NORMAL)
            self.recorded_positions_clear_btn.config(state=tk.NORMAL)
            self.disable_mouse_move_widgets()
            self.position_thread = threading.Thread(target=self.print_mouse_position)
            self.position_thread.start()

    def stop_position_thread(self):
        if self.position_thread_running:
            self.position_thread_running = False
            self.start_position_btn.config(state=tk.NORMAL)
            self.stop_position_btn.config(state=tk.DISABLED)
            self.recorded_positions_text.config(state=tk.DISABLED)
            self.recorded_positions_clear_btn.config(state=tk.DISABLED)
            self.enable_mouse_move_widgets()

    def print_mouse_position(self):
        while self.position_thread_running:
            x, y = pyautogui.position()
            position_str = f"X: {x} Y: {y}"
            self.position_label.config(text=position_str)
            time.sleep(0.1)

    def create_mouse_move_widgets(self):
        self.move_function_label = ttk.Label(self.mouse_move_frame, text="Move Mouse")
        self.move_function_label.grid(row=0, column=0, pady=10)

        self.entries = []

        for i in range(7):
            entry_frame = ttk.Frame(self.mouse_move_frame)
            entry_frame.grid(row=i+1, column=0, pady=5)

            x_label = ttk.Label(entry_frame, text=f"X{i+1}:")
            x_label.grid(row=i, column=0)
            x_entry = ttk.Entry(entry_frame, width=10)
            x_entry.grid(row=i, column=1)

            y_label = ttk.Label(entry_frame, text=f"Y{i+1}:")
            y_label.grid(row=i, column=2)
            y_entry = ttk.Entry(entry_frame, width=10)
            y_entry.grid(row=i, column=3)

            t_label = ttk.Label(entry_frame, text=f"T{i+1}:")
            t_label.grid(row=i, column=4)
            t_entry = ttk.Entry(entry_frame, width=10)
            t_entry.grid(row=i, column=5)

            click_option = tk.BooleanVar()
            click_option.set(False)
            double_click_checkbox = ttk.Checkbutton(entry_frame, text="Double Click", variable=click_option)
            double_click_checkbox.grid(row=i, column=6)

            self.entries.append((x_entry, y_entry, t_entry, click_option))

        self.loop_label = ttk.Label(self.mouse_move_frame, text="Number of Loops:")
        self.loop_label.grid(row=8, column=0, pady=5)
        self.loop_entry = ttk.Entry(self.mouse_move_frame, width=10)
        self.loop_entry.grid(row=8, column=1, padx=5)

        self.start_move_btn = ttk.Button(self.mouse_move_frame, text="Start", command=self.start_move_thread)
        self.start_move_btn.grid(row=9, column=0, pady=10)

        self.stop_move_btn = ttk.Button(self.mouse_move_frame, text="Stop", command=self.stop_move_thread, state=tk.DISABLED)
        self.stop_move_btn.grid(row=10, column=0, pady=10)

        self.move_thread_running = False

    def disable_mouse_move_widgets(self):
        for entry_set in self.entries:
            for entry in entry_set[:-1]:
                entry.config(state=tk.DISABLED)

        self.start_move_btn.config(state=tk.DISABLED)
        self.stop_move_btn.config(state=tk.DISABLED)
        self.loop_entry.config(state=tk.DISABLED)

    def enable_mouse_move_widgets(self):
        for entry_set in self.entries:
            for entry in entry_set[:-1]:
                entry.config(state=tk.NORMAL)

        self.start_move_btn.config(state=tk.NORMAL)
        self.loop_entry.config(state=tk.NORMAL)

    def start_move_thread(self):
        if not self.move_thread_running:
            self.move_thread_running = True
            self.start_move_btn.config(state=tk.DISABLED)
            self.stop_move_btn.config(state=tk.NORMAL)
            self.disable_mouse_position_widgets()
            self.move_thread = threading.Thread(target=self.click_points_loop)
            self.move_thread.start()

    def stop_move_thread(self):
        if self.move_thread_running:
            self.move_thread_running = False
            self.start_move_btn.config(state=tk.NORMAL)
            self.stop_move_btn.config(state=tk.DISABLED)
            self.enable_mouse_position_widgets()

    def click_points_loop(self):
        points = []

        for x_entry, y_entry, t_entry, click_option in self.entries:
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                t = float(t_entry.get())
                double_click = click_option.get()
                points.append((x, y, t, double_click))
            except ValueError:
                pass

        if not points:
            messagebox.showerror("Error", "Please enter valid numbers for at least one set of coordinates.")
            self.stop_move_thread()
            return

        try:
            num_loops = int(self.loop_entry.get())
            if num_loops < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the number of loops.")
            self.stop_move_thread()
            return

        for _ in range(num_loops):
            if not self.move_thread_running:
                break

            for point in points:
                if not self.move_thread_running:
                    break

                x, y, t, double_click = point
                pyautogui.moveTo(x, y)
                if double_click:
                    pyautogui.doubleClick()
                else:
                    pyautogui.click()
                time.sleep(t)

    def disable_mouse_position_widgets(self):
        self.start_position_btn.config(state=tk.DISABLED)
        self.stop_position_btn.config(state=tk.DISABLED)
        self.recorded_positions_text.config(state=tk.DISABLED)
        self.recorded_positions_clear_btn.config(state=tk.DISABLED)

    def enable_mouse_position_widgets(self):
        self.start_position_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = MouseAutomationApp()
    app.mainloop()
