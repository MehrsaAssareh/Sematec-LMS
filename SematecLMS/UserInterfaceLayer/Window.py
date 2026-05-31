import ctypes
import os
from ctypes import wintypes
from tkinter import PhotoImage
from ttkbootstrap import Window


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]


class window(Window):
    def __init__(self, size="500x300"):
        super().__init__(title="Sematec Learning Management System", themename="solar")

        self.apply_app_icon()
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.center_window(size)

    def apply_app_icon(self):
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'images', 'SematecLMS.ico')
        )
        png_icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'images', 'SematecLMS.png')
        )

        if os.path.exists(png_icon_path):
            try:
                self._app_icon_photo = PhotoImage(file=png_icon_path)
                self.iconphoto(True, self._app_icon_photo)
            except Exception:
                pass

        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

    def center_window(self, size):
        width, height = [int(value) for value in size.split("x")]
        self.update_idletasks()

        left, top, right, bottom = self.get_work_area()
        work_width = right - left
        work_height = bottom - top
        horizontal_margin = 32
        vertical_margin = 96

        width = min(width, max(200, work_width - horizontal_margin))
        height = min(height, max(200, work_height - vertical_margin))
        x = left + max(0, int((work_width - width) / 2))
        y = top + max(0, int((work_height - height) / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

    def fit_to_content(self, frame, min_width=500, min_height=300, extra_width=24, extra_height=24):
        frame.update_idletasks()

        width = max(min_width, frame.winfo_reqwidth() + extra_width)
        height = max(min_height, frame.winfo_reqheight() + extra_height)

        self.center_window(f"{width}x{height}")

    def get_work_area(self):
        work_area = RECT()
        get_work_area = 0x0030
        success = ctypes.windll.user32.SystemParametersInfoW(get_work_area, 0, ctypes.byref(work_area), 0)

        if success:
            return work_area.left, work_area.top, work_area.right, work_area.bottom

        return 0, 0, self.winfo_screenwidth(), self.winfo_screenheight()

    def show(self):
        self.mainloop()
