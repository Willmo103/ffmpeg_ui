# main.py

import os
import json
import subprocess
import logging
import logging.config
from pathlib import Path
from tkinter import (
    Tk, Frame, Label, Button, Checkbutton, IntVar, filedialog,
    messagebox, Scale, HORIZONTAL, OptionMenu, StringVar, Toplevel
)
from tkinter import ttk  # Import ttk for Notebook
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
                        "format": "[%(levelname)s] > %(asctime)s - %(name)s - %(module)s:%(lineno)s - %(message)s %(exc_info)s",
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
        output_path = filedialog.askdirectory(title="Select Output Directory")
        if not output_path:
            messagebox.showerror("Error", "Output directory is required.")
            exit(1)
        config["output_path"] = output_path
        config["mp4_dir"] = os.path.join(output_path, "mp4")
        config["gif_dir"] = os.path.join(output_path, "gif")
        for directory in [output_path, config["mp4_dir"], config["gif_dir"]]:
            try:
                os.makedirs(directory, exist_ok=True)
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Cannot create directory {directory}: {e}")
                exit(1)
        # Save config
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    else:
        for directory in [config["output_path"], config["mp4_dir"], config["gif_dir"]]:
            try:
                os.makedirs(directory, exist_ok=True)
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Cannot create directory {directory}: {e}")
                exit(1)

# Run directory check before initializing the GUI
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
        master.geometry("800x600")  # Set default larger window size

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # Convert Tab
        self.convert_tab = Frame(self.notebook)
        self.notebook.add(self.convert_tab, text="Convert")

        # Transform Tab
        self.transform_tab = Frame(self.notebook)
        self.notebook.add(self.transform_tab, text="Transform")

        # Initialize Convert and Transform Tabs
        self.init_convert_tab()
        self.init_transform_tab()

        # Frame Display
        self.init_display_frame()

    def init_convert_tab(self):
        # Buttons for conversion options
        convert_options = [
            ("Video to GIF", self.video_to_gif),
            ("GIF to Video", self.gif_to_video),
            ("Images to GIF", self.images_to_gif),
            ("GIF to Images", self.gif_to_images)
        ]

        for idx, (text, command) in enumerate(convert_options):
            btn = Button(self.convert_tab, text=text, width=20, command=command)
            btn.grid(row=idx, column=0, padx=10, pady=10, sticky='w')

    def init_transform_tab(self):
        # Size Adjustment
        size_label = Label(self.transform_tab, text="Adjust Size:")
        size_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.width_slider = Scale(self.transform_tab, from_=100, to=1920, orient=HORIZONTAL, label="Width")
        self.width_slider.set(640)
        self.width_slider.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.height_slider = Scale(self.transform_tab, from_=100, to=1080, orient=HORIZONTAL, label="Height")
        self.height_slider.set(480)
        self.height_slider.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Aspect Ratio Options
        aspect_label = Label(self.transform_tab, text="Aspect Ratio:")
        aspect_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.aspect_var = StringVar(self.transform_tab)
        self.aspect_var.set("Free")
        aspect_options = ["Free", "Square (W=L)", "16:9", "4:3"]
        self.aspect_menu = OptionMenu(self.transform_tab, self.aspect_var, *aspect_options, command=self.change_aspect_ratio)
        self.aspect_menu.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        # Direction Adjustment (Rotate)
        direction_label = Label(self.transform_tab, text="Direction:")
        direction_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        self.direction_var = StringVar(self.transform_tab)
        self.direction_var.set("None")
        direction_options = ["None", "90°", "180°", "270°"]
        self.direction_menu = OptionMenu(self.transform_tab, self.direction_var, *direction_options)
        self.direction_menu.grid(row=6, column=0, padx=10, pady=5, sticky='w')

        # Quality Scaling
        quality_label = Label(self.transform_tab, text="Quality:")
        quality_label.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        self.quality_slider = Scale(self.transform_tab, from_=1, to=31, orient=HORIZONTAL, label="FFmpeg Quality")
        self.quality_slider.set(23)  # Default FFmpeg quality
        self.quality_slider.grid(row=8, column=0, padx=10, pady=5, sticky='w')

        # Apply Transformation Button
        self.apply_transform_btn = Button(self.transform_tab, text="Apply Transformation", command=self.apply_transformation)
        self.apply_transform_btn.grid(row=9, column=0, padx=10, pady=20, sticky='w')

    def change_aspect_ratio(self, value):
        # Update width and height based on aspect ratio
        if value == "Square (W=L)":
            self.width_slider.config(state='disabled')
            self.height_slider.config(state='disabled')
            self.width_slider.set(480)
            self.height_slider.set(480)
        elif value == "16:9":
            self.width_slider.config(state='normal')
            self.height_slider.config(state='normal')
            self.width_slider.set(640)
            self.height_slider.set(360)
        elif value == "4:3":
            self.width_slider.config(state='normal')
            self.height_slider.config(state='normal')
            self.width_slider.set(640)
            self.height_slider.set(480)
        else:
            self.width_slider.config(state='normal')
            self.height_slider.config(state='normal')


    def init_display_frame(self):
        # Placeholder for frame display
        self.display_label = Label(self.master, text="Frame Display", font=("Arial", 16))
        self.display_label.pack(pady=10)

        self.frame_canvas = Label(self.master, bg='grey', width=400, height=300)
        self.frame_canvas.pack(pady=10)

        self.display_placeholder()

    def display_placeholder(self):
        # Create a placeholder image with grey background and white text
        width, height = 400, 300
        placeholder = Image.new('RGB', (width, height), color='grey')
        draw = ImageDraw.Draw(placeholder)
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
                    "-i", file_path,
                    "-vf", "fps=10,scale=320:-1:flags=lanczos",
                    "-gifflags", "+transdiff",
                    "-y",
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
                    "-i", file_path,
                    "-movflags", "faststart",
                    "-pix_fmt", "yuv420p",
                    "-vf", "scale=320:-1",
                    "-y",
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
                # FFmpeg expects a sequential image pattern
                # Ensure images are named in a sequential manner
                # e.g., frame_0001.png, frame_0002.png, etc.
                pattern = os.path.join(input_dir, "frame_%04d.png")
                cmd = [
                    FFMPEG_PATH,
                    "-framerate", "10",
                    "-i", pattern,
                    "-vf", "scale=320:-1:flags=lanczos",
                    "-y",
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
                pattern = os.path.join(output_dir, "frame_%04d.png")
                cmd = [
                    FFMPEG_PATH,
                    "-i", file_path,
                    "-vf", "fps=10",
                    pattern,
                    "-y"
                ]
                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Extracting Frames from GIF...")).start()

    def apply_transformation(self):
        # Select media to transform
        file_path = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv"), ("GIF Files", "*.gif")]
        )
        if file_path:
            # Choose output file based on input type
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".mp4", ".avi", ".mov", ".mkv"]:
                output_file = filedialog.asksaveasfilename(
                    defaultextension=ext,
                    filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")],
                    title="Save Transformed Video As"
                )
            elif ext == ".gif":
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".gif",
                    filetypes=[("GIF Files", "*.gif")],
                    title="Save Transformed GIF As"
                )
            else:
                messagebox.showerror("Unsupported Format", "Selected file format is not supported.")
                return

            if output_file:
                # Build FFmpeg command based on transformations
                vf_filters = []

                # Size adjustment
                width = self.width_slider.get()
                height = self.height_slider.get()
                vf_filters.append(f"scale={width}:{height}")

                # Direction adjustment
                direction = self.direction_var.get()
                if direction == "90°":
                    vf_filters.append("transpose=1")
                elif direction == "180°":
                    vf_filters.append("transpose=2,transpose=2")
                elif direction == "270°":
                    vf_filters.append("transpose=2")

                # Combine filters
                vf = ",".join(vf_filters)

                # Quality scaling (for videos: CRF; for GIFs: use appropriate options)
                quality = self.quality_slider.get()

                if ext in [".mp4", ".avi", ".mov", ".mkv"]:
                    # For videos, use CRF for quality
                    cmd = [
                        FFMPEG_PATH,
                        "-i", file_path,
                        "-vf", vf,
                        "-c:v", "libx264",
                        "-crf", str(quality),
                        "-y",
                        output_file
                    ]
                elif ext == ".gif":
                    # For GIFs, quality control is different; adjust fps and scaling
                    cmd = [
                        FFMPEG_PATH,
                        "-i", file_path,
                        "-vf", vf,
                        "-y",
                        output_file
                    ]
                else:
                    messagebox.showerror("Unsupported Format", "Selected file format is not supported.")
                    return

                threading.Thread(target=self.run_ffmpeg_command, args=(cmd, "Applying Transformation...")).start()

    def run_ffmpeg_command(self, cmd, message):
        logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
        # Show progress window
        self.show_progress(message)
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            logger.info(f"{message} Completed successfully. Output: {result.stdout.decode()}")
            messagebox.showinfo("Success", f"{message} Completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"{message} Failed. Error: {e.stderr.decode()}")
            messagebox.showerror("Error", f"{message} Failed.\nError: {e.stderr.decode()}")
        finally:
            # Close progress window
            if hasattr(self, 'progress_window') and self.progress_window.winfo_exists():
                self.progress_window.destroy()

    def show_progress(self, message):
        self.progress_window = Toplevel(self.master)
        self.progress_window.title("Processing")
        self.progress_window.geometry("300x100")
        self.progress_window.grab_set()  # Make window modal

        label = Label(self.progress_window, text=message)
        label.pack(pady=20)

        # Simple progress indicator
        progress = ttk.Progressbar(self.progress_window, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill='x')
        progress.start()

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = FFmpegApp(root)
    root.mainloop()
