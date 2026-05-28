from io import BytesIO
import mimetypes
import os
from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError
from tkinter import filedialog
from ttkbootstrap import Button, Frame, Label, OUTLINE, INFO, DANGER


class PersonPhotoPicker(Frame):
    def __init__(self, master, preview_size=(96, 96), editable=True):
        super().__init__(master)

        self.preview_size = preview_size
        self.photo_content = None
        self.photo_file_name = None
        self.photo_content_type = None
        self.remove_photo = False
        self._photo_image = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.preview_label = Label(self, text='No Photo', anchor='center', width=18)
        self.preview_label.grid(row=0, column=0, rowspan=2, padx=(0, 8), pady=2, sticky='nsew')

        if editable:
            select_button = Button(self, text='Select Photo', bootstyle=OUTLINE + INFO, command=self.select_photo)
            select_button.grid(row=0, column=1, padx=0, pady=(0, 4), sticky='ew')

            remove_button = Button(self, text='Remove', bootstyle=OUTLINE + DANGER, command=self.remove_current_photo)
            remove_button.grid(row=1, column=1, padx=0, pady=(4, 0), sticky='ew')

        self.show_placeholder()

    def select_photo(self):
        file_path = filedialog.askopenfilename(
            title='Select Person Photo',
            filetypes=[
                ('Image files', '*.jpg *.jpeg *.png'),
                ('JPEG files', '*.jpg *.jpeg'),
                ('PNG files', '*.png')
            ]
        )
        if not file_path:
            return

        with open(file_path, 'rb') as photo_file:
            content = photo_file.read()

        self.set_photo_content(
            content,
            os.path.basename(file_path),
            self.get_content_type(file_path)
        )

    def set_photo_content(self, content, file_name=None, content_type=None):
        if content is None:
            self.show_placeholder()
            return

        image = self.load_image(content)
        if image is None:
            self.show_placeholder()
            return

        self.photo_content = content
        self.photo_file_name = file_name
        self.photo_content_type = content_type or 'image/jpeg'
        self.remove_photo = False
        self.render_image(image)

    def set_database_photo(self, photo):
        self.photo_content = None
        self.photo_file_name = None
        self.photo_content_type = None
        self.remove_photo = False

        if not photo:
            self.show_placeholder()
            return

        self.set_photo_content(
            photo.get('content'),
            photo.get('file_name'),
            photo.get('content_type')
        )
        self.photo_content = None

    def remove_current_photo(self):
        self.photo_content = None
        self.photo_file_name = None
        self.photo_content_type = None
        self.remove_photo = True
        self.show_placeholder()

    def clear(self):
        self.photo_content = None
        self.photo_file_name = None
        self.photo_content_type = None
        self.remove_photo = False
        self.show_placeholder()

    def get_change(self):
        return {
            'photo_content': self.photo_content,
            'photo_file_name': self.photo_file_name,
            'photo_content_type': self.photo_content_type,
            'remove_photo': self.remove_photo
        }

    def load_image(self, content):
        try:
            image = Image.open(BytesIO(content))
            return ImageOps.exif_transpose(image).convert('RGB')
        except (UnidentifiedImageError, OSError):
            return None

    def render_image(self, image):
        image.thumbnail(self.preview_size, Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', self.preview_size, '#F4F7F9')
        x = (self.preview_size[0] - image.width) // 2
        y = (self.preview_size[1] - image.height) // 2
        canvas.paste(image, (x, y))
        self._photo_image = ImageTk.PhotoImage(canvas)
        self.preview_label.configure(image=self._photo_image, text='')

    def show_placeholder(self):
        canvas = Image.new('RGB', self.preview_size, '#EEF3F5')
        self._photo_image = ImageTk.PhotoImage(canvas)
        self.preview_label.configure(image=self._photo_image, text='No Photo', compound='center')

    def get_content_type(self, file_path):
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type in ('image/jpeg', 'image/png'):
            return content_type

        extension = os.path.splitext(file_path)[1].lower()
        if extension == '.png':
            return 'image/png'

        return 'image/jpeg'
