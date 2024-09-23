# main_app.py

import os
import json
import subprocess
import logging
import logging.config
from pathlib import Path
from tkinter import (
    Tk, Frame, Label, Button, Checkbutton, IntVar, filedialog,
    messagebox, Scale, HORIZONTAL, OptionMenu, StringVar, ttk, Toplevel
)
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading

# Configuration and Logging Setup
CONFIG_PATH = "conf.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Create default config
        default_config = {
            "logging_config": {
                "version": 1,
                "formatters": {
                    "debug": {
                        "format": "[%(levelname)s] > %(asctime)s - %(name)s - %(module)s:%(lineno)s - %(message)s",
                        "datefmt": "%Y-%m-%d %H:%M:%S"
                    }
                },
                "handlers": {
                    "file": {
                        "class": "logging.FileHandler",
                        "level": "DEBUG",
                        "formatter": "debug",
                        "filename": "ffmpeg_app.log",
                        "mode": "a",
                        "encoding": "utf-8"
                    }
                },
                "root": {
                    "level": "DEBUG",
                    "handlers": [
                        "file"
                    ]
                }
            },
            "logger_name": "ffmpeg_app",
            "output_path": "",
            "log_file": "ffmpeg_app.log",
            "mp4_dir": "",
            "gif_dir": ""
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)


config = load_config()

# Setup logging
logging.config.dictConfig(config["logging_config"])
logger = logging.getLogger(config["logger_name"])

# Ensure output directories
def ensure_directories():
    output_path = config.get("output_path")
    if not output_path:
        root = Tk()
        root.withdraw()  # Hide the main window
        output_path = filedialog.askdirectory(title="Select Output Directory")
        if not output_path:
            messagebox.showerror("Error", "Output directory is required.")
            exit(1)
        config["output_path"] = output_path
        config["mp4_dir"] = os.path.join(output_path, "mp4")
        config["gif_dir"] = os.path.join(output_path, "gif")
        for directory in [output_path, config["mp4_dir"], config["gif_dir"]]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except PermissionError as e:
                    messagebox.showerror("Permission Error", f"Cannot create directory: {directory}\n{e}")
                    exit(1)
        # Save config
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    else:
        for directory in [config["output_path"], config["mp4_dir"], config["gif_dir"]]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except PermissionError as e:
                    messagebox.showerror("Permission Error", f"Cannot create directory: {directory}\n{e}")
                    exit(1)

ensure_directories()

# FFmpeg Path
FFMPEG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin")
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")

if not os.path.exists(FFMPEG_PATH):
    messagebox.showerror("FFmpeg Not Found", "FFmpeg is not installed. Please run setup_ffmpeg.py first.")
    exit(1)

# Main Application Class
class FFmpegApp:
    def __init__(self, master):
        self.master = master
        master.title("FFmpeg Application")
        master.geometry("800x600")  # Set a larger default size

        # Create Tabs
        self.tab_control = ttk.Notebook(master)

        self.convert_tab = ttk.Frame(self.tab_control)
        self.transform_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.convert_tab, text='Convert')
        self.tab_control.add(self.transform_tab, text='Transform')
        self.tab_control.pack(expand=1, fill='both')

        # Initialize Convert and Transform Tabs
        self.init_convert_tab()
        self.init_transform_tab()

    def init_convert_tab(self):
        # Conversion Options
        convert_frame = Frame(self.convert_tab)
        convert_frame.pack(pady=10, padx=10, fill='x')

        Label(convert_frame, text="Conversion Options:", font=("Helvetica", 14)).pack(anchor='w')

        # Video to GIF
        self.video_to_gif_btn = Button(convert_frame, text="Video to GIF", command=self.video_to_gif)
        self.video_to_gif_btn.pack(fill='x', pady=5)

        # GIF to Video
        self.gif_to_video_btn = Button(convert_frame, text="GIF to Video", command=self.gif_to_video)
        self.gif_to_video_btn.pack(fill='x', pady=5)

        # Images to GIF
        self.images_to_gif_btn = Button(convert_frame, text="Images to GIF", command=self.images_to_gif)
        self.images_to_gif_btn.pack(fill='x', pady=5)

        # GIF to Images
        self.gif_to_images_btn = Button(convert_frame, text="GIF to Images", command=self.gif_to_images)
        self.gif_to_images_btn.pack(fill='x', pady=5)

        # Frame Display
        self.display_label = Label(self.convert_tab, text="Frame Display")
        self.display_label.pack(pady=10)
        self.frame_canvas = Label(self.convert_tab)
        self.frame_canvas.pack(pady=5)

        # Placeholder
        self.display_placeholder()

    def init_transform_tab(self):
        # Transformation Options
        transform_frame = Frame(self.transform_tab)
        transform_frame.pack(pady=10, padx=10, fill='x')

        Label(transform_frame, text="Transformation Options:", font=("Helvetica", 14)).pack(anchor='w')

        # Size Adjustment
        size_frame = Frame(transform_frame)
        size_frame.pack(fill='x', pady=5)

        Label(size_frame, text="Width:").grid(row=0, column=0, sticky='w')
        self.width_slider = Scale(size_frame, from_=100, to=1920, orient=HORIZONTAL)
        self.width_slider.grid(row=0, column=1, padx=5)

        Label(size_frame, text="Height:").grid(row=1, column=0, sticky='w')
        self.height_slider = Scale(size_frame, from_=100, to=1080, orient=HORIZONTAL)
        self.height_slider.grid(row=1, column=1, padx=5)

        # Aspect Ratio Options
        aspect_frame = Frame(transform_frame)
        aspect_frame.pack(fill='x', pady=5)

        Label(aspect_frame, text="Aspect Ratio:").grid(row=0, column=0, sticky='w')
        self.aspect_var = StringVar(self.transform_tab)
        self.aspect_var.set("Free")
        aspect_options = ["Free", "Square (W=L)", "16:9", "4:3"]
        self.aspect_menu = OptionMenu(aspect_frame, self.aspect_var, *aspect_options, command=self.change_aspect_ratio)
        self.aspect_menu.grid(row=0, column=1, padx=5, sticky='w')

        # Transformation Buttons
        transform_buttons_frame = Frame(transform_frame)
        transform_buttons_frame.pack(pady=10)

        self.select_transform_btn = Button(transform_buttons_frame, text="Select Video/GIF for Transformation", command=self.select_transform_file)
        self.select_transform_btn.pack(fill='x', pady=5)

        self.apply_transform_btn = Button(transform_buttons_frame, text="Apply Transformation", command=self.apply_transformation, state="disabled")
        self.apply_transform_btn.pack(fill='x', pady=5)

    def display_placeholder(self):
        # Create a placeholder image with grey background and white text
        placeholder = Image.new('RGB', (400, 300), color='grey')
        draw = ImageDraw.Draw(placeholder)
        text = "No Media Selected"
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (placeholder.width - text_width) / 2
        text_y = (placeholder.height - text_height) / 2
        draw.text((text_x, text_y), text, fill='white', font=font)

        self.photo = ImageTk.PhotoImage(placeholder)
        self.frame_canvas.config(image=self.photo)

    def video_to_gif(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")]
        )
        if file_path:
            output_file = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif")],
                title="Save GIF As"
            )
            if output_file:
                cmd = [
                    FFMPEG_PATH,
                    '-i', file_path,
                    '-vf', 'fps=10,scale=320:-1:flags=lanczos',
                    '-gifflags', '+transdiff',
                    '-y',  # Overwrite output file if it exists
                    output_file
                ]
                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Converting Video to GIF...")).start()

    def gif_to_video(self):
        file_path = filedialog.askopenfilename(
            title="Select GIF File",
            filetypes=[("GIF Files", "*.gif")]
        )
        if file_path:
            output_file = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 Files", "*.mp4")],
                title="Save Video As"
            )
            if output_file:
                cmd = [
                    FFMPEG_PATH,
                    '-f', 'gif',
                    '-i', file_path,
                    '-movflags', 'faststart',
                    '-pix_fmt', 'yuv420p',
                    '-vf', 'scale=320:-1',
                    '-y',  # Overwrite output file if it exists
                    output_file
                ]
                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Converting GIF to Video...")).start()

    def images_to_gif(self):
        input_dir = filedialog.askdirectory(title="Select Directory with Images")
        if input_dir:
            output_file = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif")],
                title="Save GIF As"
            )
            if output_file:
                # Ensure all images are sorted
                images_pattern = os.path.join(input_dir, "frame_%04d.png")
                cmd = [
                    FFMPEG_PATH,
                    '-framerate', '10',
                    '-i', images_pattern,
                    '-vf', 'scale=320:-1:flags=lanczos',
                    '-y',  # Overwrite output file if it exists
                    output_file
                ]
                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Creating GIF from Images...")).start()

    def gif_to_images(self):
        file_path = filedialog.askopenfilename(
            title="Select GIF File",
            filetypes=[("GIF Files", "*.gif")]
        )
        if file_path:
            output_dir = filedialog.askdirectory(title="Select Output Directory for Frames")
            if output_dir:
                images_pattern = os.path.join(output_dir, "frame_%04d.png")
                cmd = [
                    FFMPEG_PATH,
                    '-i', file_path,
                    '-vf', 'fps=10',
                    images_pattern,
                    '-y'  # Overwrite output files if they exist
                ]
                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Extracting Frames from GIF...")).start()

    def select_transform_file(self):
        self.transform_file_path = filedialog.askopenfilename(
            title="Select Video or GIF File",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv"), ("GIF Files", "*.gif")]
        )
        if self.transform_file_path:
            self.apply_transform_btn.config(state="normal")
            self.display_frame(self.transform_file_path)

    def apply_transformation(self):
        if not hasattr(self, 'transform_file_path'):
            messagebox.showerror("Error", "No file selected for transformation.")
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4"), ("GIF Files", "*.gif")],
            title="Save Transformed File As"
        )
        if not output_file:
            return

        width = self.width_slider.get()
        height = self.height_slider.get()

        # Determine if the output is GIF or Video based on the extension
        ext = os.path.splitext(output_file)[1].lower()
        if ext == ".gif":
            output_format = "gif"
        else:
            output_format = "mp4"

        scale_filter = f"scale={width}:{height}:flags=lanczos"

        if output_format == "gif":
            cmd = [
                FFMPEG_PATH,
                '-i', self.transform_file_path,
                '-vf', scale_filter,
                '-y',
                output_file
            ]
        else:
            cmd = [
                FFMPEG_PATH,
                '-i', self.transform_file_path,
                '-vf', scale_filter,
                '-movflags', 'faststart',
                '-pix_fmt', 'yuv420p',
                '-y',
                output_file
            ]

        threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Applying Transformation...")).start()

    def change_aspect_ratio(self, value):
        if value == "Free":
            self.width_slider.config(state="normal")
            self.height_slider.config(state="normal")
            self.width_slider.config(command=None)
            self.height_slider.config(command=None)
        elif value == "Square (W=L)":
            self.height_slider.set(self.width_slider.get())
            self.height_slider.config(state="disabled")
            self.width_slider.config(command=self.update_square)
        elif value == "16:9":
            calculated_height = int(self.width_slider.get() * 9 / 16)
            self.height_slider.set(calculated_height)
            self.height_slider.config(state="disabled")
            self.width_slider.config(command=self.update_16_9)
        elif value == "4:3":
            calculated_height = int(self.width_slider.get() * 3 / 4)
            self.height_slider.set(calculated_height)
            self.height_slider.config(state="disabled")
            self.width_slider.config(command=self.update_4_3)

    def update_square(self, val):
        try:
            val = int(val)
            self.height_slider.set(val)
        except ValueError:
            pass

    def update_16_9(self, val):
        try:
            val = int(val)
            calculated_height = int(val * 9 / 16)
            self.height_slider.set(calculated_height)
        except ValueError:
            pass

    def update_4_3(self, val):
        try:
            val = int(val)
            calculated_height = int(val * 3 / 4)
            self.height_slider.set(calculated_height)
        except ValueError:
            pass

    def display_frame(self, file_path, first=True):
        # Check file size or duration
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # 50 MB limit for example
            logger.info("File too large for frame display.")
            self.display_placeholder()
            return

        ext = os.path.splitext(file_path)[1].lower()
        temp_frame = os.path.join(config["output_path"], "temp_frame.png")

        try:
            if ext == ".gif":
                with Image.open(file_path) as img:
                    frame = img.convert('RGBA')
                    frame.save(temp_frame)
            else:
                # Use FFmpeg to extract frame
                cmd = [
                    FFMPEG_PATH,
                    "-i", file_path,
                    "-vf", "select=eq(n\,0)",
                    "-q:v", "3",
                    temp_frame
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # Open the frame image
            with Image.open(temp_frame) as img:
                img.thumbnail((400, 400))
                self.photo = ImageTk.PhotoImage(img)
                self.frame_canvas.config(image=self.photo)

            # Remove the temp frame
            os.remove(temp_frame)

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e}")
            messagebox.showerror("Error", "Failed to extract frame from video.")
            self.display_placeholder()
        except Exception as e:
            logger.error(f"Error displaying frame: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.display_placeholder()

    def run_ffmpeg_command(self, cmd, message):
        try:
            self.show_progress(message)
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            messagebox.showinfo("Success", f"{message} Completed successfully.")
            logger.info(f"{message} Completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"{message} Failed: {e.stderr.decode()}")
            messagebox.showerror("Error", f"{message} Failed.")
        finally:
            if hasattr(self, 'progress_window') and self.progress_window.winfo_exists():
                self.progress_window.destroy()

    def show_progress(self, message):
        self.progress_window = Toplevel(self.master)
        self.progress_window.title("Processing")
        self.progress_window.geometry("300x100")
        Label(self.progress_window, text=message).pack(pady=20)
        self.progress_bar = ttk.Progressbar(self.progress_window, mode='indeterminate')
        self.progress_bar.pack(pady=10, padx=20, fill='x')
        self.progress_bar.start()

if __name__ == "__main__":
    root = Tk()
    app = FFmpegApp(root)
    root.mainloop()
