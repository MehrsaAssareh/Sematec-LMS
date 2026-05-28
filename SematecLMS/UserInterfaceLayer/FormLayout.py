from ttkbootstrap import Button, Combobox, DateEntry, Entry, Label

READONLY_VALUE_FOREGROUND = '#1E9E93'
READONLY_VALUE_FONT = ('Arial', 10, 'bold')


def apply_form_field_layout(form_frame, entry_width=32, combo_width=30, date_width=27, text_width=80):
    for child in form_frame.winfo_children():
        grid_info = child.grid_info()
        if not grid_info:
            continue

        column = int(grid_info.get('column', 0))
        columnspan = int(grid_info.get('columnspan', 1))

        if isinstance(child, Label):
            if columnspan > 1:
                continue

            if column in (0, 2):
                child.grid_configure(padx=(10, 2), pady=3, sticky='w')
            continue

        if isinstance(child, Combobox):
            child.configure(width=combo_width)
            child.grid_configure(padx=(2, 10), pady=3, sticky='ew')
            continue

        if isinstance(child, Entry):
            child.configure(width=entry_width)
            child.grid_configure(padx=(2, 10), pady=3, sticky='ew')
            continue

        if isinstance(child, DateEntry):
            child.configure(width=date_width)
            child.grid_configure(padx=(2, 10), pady=3, sticky='ew')
            continue

        if isinstance(child, Button):
            child.grid_configure(pady=4)
            continue

        if child.__class__.__name__ == 'ScrolledText':
            child.configure(width=text_width)
            child.grid_configure(padx=(2, 10), pady=3, sticky='ew')
            continue

        apply_form_field_layout(child, entry_width, combo_width, date_width, text_width)


def apply_readonly_value_style(*labels):
    for label in labels:
        label.configure(foreground=READONLY_VALUE_FOREGROUND, font=READONLY_VALUE_FONT)
