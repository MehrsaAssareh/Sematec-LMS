from queue import Empty, Queue
from threading import Thread
from tkinter import messagebox as msg


def initialize_lazy_page(frame):
    frame._page_data_loaded = False
    frame._page_loading = False
    frame._page_pending_refresh = False
    frame._page_refresh_generation = 0
    frame._page_refresh_job = None
    frame._page_refresh_poll_job = None
    frame._page_refresh_queue = None


def mark_page_stale(frame):
    frame._page_data_loaded = False


def schedule_page_refresh(frame):
    queue_page_refresh(frame)


def refresh_page_now(frame):
    queue_page_refresh(frame, force=True)


def queue_page_refresh(frame, force=False):
    if frame._page_data_loaded and not force:
        return

    if frame._page_loading:
        frame._page_pending_refresh = True
        return

    if frame._page_refresh_job is not None:
        if not force:
            return

        frame.after_cancel(frame._page_refresh_job)
        frame._page_refresh_job = None

    frame._page_refresh_job = frame.after(1, lambda: run_page_refresh(frame))


def run_page_refresh(frame):
    frame._page_refresh_job = None

    if hasattr(frame, 'load_page_data') and hasattr(frame, 'apply_page_data'):
        start_background_refresh(frame)
        return

    try:
        frame.refresh_page()
        frame._page_data_loaded = True
    except Exception as error:
        show_refresh_error(frame, error)


def start_background_refresh(frame):
    frame._page_loading = True
    frame._page_pending_refresh = False
    frame._page_data_loaded = False
    frame._page_refresh_generation += 1

    generation = frame._page_refresh_generation
    request = frame.get_refresh_request() if hasattr(frame, 'get_refresh_request') else None
    refresh_queue = Queue(maxsize=1)
    frame._page_refresh_queue = refresh_queue

    Thread(
        target=load_page_data,
        args=(frame, request, refresh_queue),
        daemon=True
    ).start()
    frame._page_refresh_poll_job = frame.after(25, lambda: poll_page_refresh(frame, generation, refresh_queue))


def load_page_data(frame, request, refresh_queue):
    try:
        refresh_queue.put((frame.load_page_data(request), None))
    except Exception as error:
        refresh_queue.put((None, error))


def poll_page_refresh(frame, generation, refresh_queue):
    try:
        data, error = refresh_queue.get_nowait()
    except Empty:
        frame._page_refresh_poll_job = frame.after(
            25,
            lambda: poll_page_refresh(frame, generation, refresh_queue)
        )
        return

    frame._page_refresh_poll_job = None

    if generation == frame._page_refresh_generation:
        if error:
            show_refresh_error(frame, error)
        else:
            frame.apply_page_data(data)
            frame._page_data_loaded = True

    frame._page_loading = False
    frame._page_refresh_queue = None

    if frame._page_pending_refresh:
        frame._page_pending_refresh = False
        queue_page_refresh(frame, force=True)


def show_refresh_error(frame, error):
    if hasattr(frame, 'show_refresh_error'):
        frame.show_refresh_error(error)
        return

    msg.showerror('Page Load Failed', str(error))
