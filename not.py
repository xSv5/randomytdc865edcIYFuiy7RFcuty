import requests
import tempfile
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time
import threading
import os
import sys


class LogoWindowApp:
    ERROR_CODES = {
        "DOWNLOAD_FAILED": 101,
        "IMAGE_LOAD_FAILED": 102,
    }

    def __init__(self, logo_url, display_text):
        self.logo_url = logo_url
        self.display_text = display_text  # Text to display in the window
        self.temp_image_path = None
        self.root = tk.Tk()
        self.is_animation_active = True
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_width = int(self.screen_width * 0.15)
        self.window_height = int(self.screen_height * 0.08)
        self.initial_x = self.screen_width
        self.vertical_position = self.screen_height - self.window_height - int(self.screen_height * 0.05)

    def download_logo(self):
        try:
            response = requests.get(self.logo_url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
                self.temp_image_path = temp_image_file.name
                temp_image_file.write(response.content)
            print(f"Logo image downloaded to: {self.temp_image_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error {self.ERROR_CODES['DOWNLOAD_FAILED']}: Failed to download the logo image. {e}")
            raise SystemExit(self.ERROR_CODES["DOWNLOAD_FAILED"])

    def load_logo_image(self):
        try:
            logo_image = Image.open(self.temp_image_path)
            logo_width, logo_height = logo_image.size
            aspect_ratio = logo_width / logo_height

            if logo_width > logo_height:
                new_width = int(self.window_width * 0.5)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = int(self.window_height * 0.5)
                new_width = int(new_height * aspect_ratio)

            return logo_image.resize((new_width, new_height))
        except IOError as e:
            print(f"Error {self.ERROR_CODES['IMAGE_LOAD_FAILED']}: Unable to load logo image. {e}")
            raise SystemExit(self.ERROR_CODES["IMAGE_LOAD_FAILED"])

    def setup_window(self):
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', 1)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.initial_x}+{self.vertical_position}")
        self.root.configure(bg='black')

    def add_logo_and_text(self, logo_image):
        img_tk = ImageTk.PhotoImage(logo_image)
        logo_label = Label(self.root, image=img_tk, bg='black')
        logo_label.image = img_tk
        logo_label.pack(side='left', padx=10, pady=5)

        text_label = Label(
            self.root, text=self.display_text, fg="white", bg="black", font=("Arial", 12, "bold")
        )
        text_label.pack(side='left', padx=10, pady=5)

    @staticmethod
    def ease_out(t, b, c, d):
        t /= d
        t -= 1
        return c * (t * t * t + 1) + b

    def animate_window(self, current_x, start_time, is_backwards=False):
        if not self.is_animation_active:
            return

        elapsed_time = time.time() - start_time
        total_duration = 0.6

        if not is_backwards:
            if current_x > (self.screen_width - self.window_width):
                new_x = self.ease_out(elapsed_time, self.initial_x, self.screen_width - self.window_width - self.initial_x, total_duration)
                self.root.geometry(f"{self.window_width}x{self.window_height}+{int(new_x)}+{self.vertical_position}")
                self.root.after(10, self.animate_window, new_x, start_time)
            else:
                self.root.geometry(f"{self.window_width}x{self.window_height}+{self.screen_width - self.window_width}+{self.vertical_position}")
                self.root.after(3000, self.move_back)
        else:
            if current_x < self.initial_x:
                new_x = self.ease_out(
                    elapsed_time,
                    self.screen_width - self.window_width,
                    self.initial_x - (self.screen_width - self.window_width),
                    total_duration,
                )
                self.root.geometry(f"{self.window_width}x{self.window_height}+{int(new_x)}+{self.vertical_position}")
                self.root.after(10, self.animate_window, new_x, start_time, True)
            else:
                self.root.geometry(f"{self.window_width}x{self.window_height}+{self.initial_x}+{self.vertical_position}")
                self.is_animation_active = False

    def move_back(self):
        start_time = time.time()
        self.animate_window(self.screen_width - self.window_width, start_time, True)

    def start_animation(self):
        start_time = time.time()
        self.animate_window(self.initial_x, start_time)

    @staticmethod
    def close_app():
        print("Closing application in 5 seconds...")
        time.sleep(5)
        os._exit(0)

    def run(self):
        self.download_logo()
        logo_image = self.load_logo_image()
        self.setup_window()
        self.add_logo_and_text(logo_image)

        threading.Thread(target=self.close_app).start()
        self.start_animation()
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <display_text>")
        sys.exit(1)

    LOGO_URL = "https://i.ibb.co/gy26xMr/download.png"
    DISPLAY_TEXT = " ".join(sys.argv[1:])  # Join all arguments to handle spaces

    app = LogoWindowApp(LOGO_URL, DISPLAY_TEXT)
    app.run()
