# main_app.py

import os
import json
import shutil
import subprocess
import logging
import logging.config
from pathlib import Path
from tkinter import (
    filedialog,
    messagebox,
    StringVar, IntVar,
)
from PIL import Image, ImageTk
import threading
import sys
import platform
import webbrowser

# Install ttkbootstrap if not already installed
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ttkbootstrap"])
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *

# Configuration and Logging Setup
CONFIG_PATH = "conf.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Move conf.example.json to conf.json if it exists
        if os.path.exists("conf.example.json"):
            shutil.copy("conf.example.json", "conf.json")
        else:
            # Create a default conf.json if conf.example.json doesn't exist
            default_config = {
                "logging_config": {
                    "version": 1,
                    "handlers": {
                        "file": {
                            "class": "logging.FileHandler",
                            "filename": "app.log",
                            "formatter": "default",
                        },
                    },
                    "formatters": {
                        "default": {
                            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        },
                    },
                    "loggers": {
                        "FFmpegApp": {
                            "handlers": ["file"],
                            "level": "INFO",
                        }
                    },
                },
                "logger_name": "FFmpegApp",
                "output_path": "",
                "mp4_dir": "",
                "gif_dir": "",
                "max_width": 1920,
                "max_height": 1032
            }
            with open("conf.json", "w") as f:
                json.dump(default_config, f, indent=4)
        # Load the copied or default file
        with open("conf.json") as j:
            config = json.load(j)
            # Set default max widths and heights if not present
            config.setdefault("max_width", 1920)
            config.setdefault("max_height", 1032)
            return config
    else:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            # Ensure max_width and max_height are present
            config.setdefault("max_width", 1920)
            config.setdefault("max_height", 1032)
            return config


config = load_config()

# Setup logging
logging.config.dictConfig(config.get("logging_config", {
    "version": 1,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "loggers": {
        "FFmpegApp": {
            "handlers": ["file"],
            "level": "INFO",
        },
    },
}))
logger = logging.getLogger(config.get("logger_name", "FFmpegApp"))


# Ensure output directories
def ensure_directories():
    output_path = config.get("output_path")
    if not output_path:
        root = tb.Window()
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
                    messagebox.showerror(
                        "Permission Error", f"Cannot create directory: {directory}\n{e}"
                    )
                    exit(1)
        # Save config
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    else:
        for directory in [config["output_path"], config["mp4_dir"], config["gif_dir"]]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except PermissionError as e:
                    if os.path.exists(directory):
                        pass
                    messagebox.showerror(
                        "Permission Error", f"Cannot create directory: {directory}\n{e}"
                    )
                    exit(1)


ensure_directories()

# FFmpeg Path
FFMPEG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin")
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe") if platform.system() == "Windows" else "ffmpeg"

FFPROBE_PATH = os.path.join(os.path.dirname(FFMPEG_PATH), "ffprobe.exe") if platform.system() == "Windows" else "ffprobe"

if not os.path.exists(FFMPEG_PATH):
    messagebox.showerror(
        "FFmpeg Not Found", "FFmpeg is not installed. Please run setup_ffmpeg.py first."
    )
    exit(1)


# Main Application Class
class FFmpegApp:
    def __init__(self, master):
        self.master = master
        master.title("FFmpeg Application")
        master.geometry("900x800")  # Increased size for more controls
        master.resizable(False, False)

        # Style Configuration using ttkbootstrap
        self.style = tb.Style(theme="darkly")  # Default to dark mode

        # Variables for aspect ratio lock
        self.ratio_lock_var = IntVar(value=1)  # Enabled by default
        self.sort_var = IntVar(value=1)  # Enabled by default
        self.original_ratio = 1.0

        # Main Frame
        self.main_frame = tb.Frame(master)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Theme Toggle Button
        self.theme_toggle = tb.Checkbutton(
            self.main_frame,
            text="Light Mode",
            command=self.toggle_theme,
            bootstyle="switch",
            width=12,
            padding=5,
        )
        self.theme_toggle.pack(anchor="e", pady=(0, 10))

        # Conversion and Transformation Options
        self.init_main_controls()

    def init_main_controls(self):
        # Operation Selection
        operation_frame = tb.Frame(self.main_frame)
        operation_frame.pack(fill="x", pady=10)

        tb.Label(
            operation_frame, text="Select Operation:", font=("Helvetica", 14, "bold")
        ).pack(anchor="w")

        self.operation_var = StringVar()
        self.operation_var.set("Video to GIF")
        operations = [
            "Video to GIF",
            "GIF to Video",
            "Images to GIF",
            "GIF to Images",
            "Video to Images",
            "Images to Video",
        ]
        self.operation_menu = tb.OptionMenu(
            operation_frame,
            self.operation_var,
            *operations,
            command=self.update_options,
            bootstyle="info",
            # width=20,  # Removed unsupported 'width' option
        )
        self.operation_menu.pack(anchor="w", pady=5)

        # Dynamic Options Frame
        self.options_frame = tb.Frame(self.main_frame)
        self.options_frame.pack(fill="both", pady=10)

        # Common Options
        # Frames Per Second
        fps_frame = tb.Frame(self.options_frame)
        fps_frame.pack(fill="x", pady=5)
        tb.Label(fps_frame, text="Frames Per Second (FPS):").pack(side="left")
        self.fps_slider = tb.Scale(
            fps_frame,
            from_=1,
            to=60,
            orient=HORIZONTAL,
            length=200,
            bootstyle="warning",
            command=self.on_fps_slider_change,
        )
        self.fps_slider.set(10)
        self.fps_slider.pack(side="left", padx=10)
        self.fps_entry = tb.Entry(fps_frame, width=5)
        self.fps_entry.insert(0, "10")
        self.fps_entry.pack(side="left")
        self.fps_entry.bind("<Return>", self.update_fps_slider)

        # Aspect Ratio Lock
        ratio_frame = tb.Frame(self.options_frame)
        ratio_frame.pack(fill="x", pady=5)
        self.ratio_lock = tb.Checkbutton(
            ratio_frame,
            text="Lock Aspect Ratio",
            variable=self.ratio_lock_var,
            command=self.toggle_ratio_lock,
            bootstyle="primary",
        )
        self.ratio_lock.pack(anchor="w")

        # Width and Height
        size_frame = tb.Frame(self.options_frame)
        size_frame.pack(fill="x", pady=5)

        tb.Label(size_frame, text="Width:").grid(row=0, column=0, sticky="w")
        self.width_slider = tb.Scale(
            size_frame,
            from_=128,
            to=config.get("max_width", 1920),
            orient=HORIZONTAL,
            length=300,
            bootstyle="success",
            command=self.on_width_change,
        )
        self.width_slider.set(512)
        self.width_slider.grid(row=0, column=1, padx=10)
        self.width_entry = tb.Entry(size_frame, width=5)
        self.width_entry.insert(0, "512")
        self.width_entry.grid(row=0, column=2)
        self.width_entry.bind("<Return>", self.update_width_slider)

        tb.Label(size_frame, text="Height:").grid(row=1, column=0, sticky="w")
        self.height_slider = tb.Scale(
            size_frame,
            from_=128,
            to=config.get("max_height", 1032),
            orient=HORIZONTAL,
            length=300,
            bootstyle="success",
            command=self.on_height_change,
        )
        self.height_slider.set(512)
        self.height_slider.grid(row=1, column=1, padx=10)
        self.height_entry = tb.Entry(size_frame, width=5)
        self.height_entry.insert(0, "512")
        self.height_entry.grid(row=1, column=2)
        self.height_entry.bind("<Return>", self.update_height_slider)

        # Quality Slider
        quality_frame = tb.Frame(self.options_frame)
        quality_frame.pack(fill="x", pady=5)
        tb.Label(quality_frame, text="Quality:").pack(side="left")
        self.quality_slider = tb.Scale(
            quality_frame, from_=1, to=100, orient=HORIZONTAL, length=200, bootstyle="danger"
        )
        self.quality_slider.set(75)
        self.quality_slider.pack(side="left", padx=10)
        self.quality_entry = tb.Entry(quality_frame, width=5)
        self.quality_entry.insert(0, "75")
        self.quality_entry.pack(side="left")
        self.quality_entry.bind("<Return>", self.update_quality_slider)

        # Image Type Selection
        image_type_frame = tb.Frame(self.options_frame)
        image_type_frame.pack(fill="x", pady=5)
        tb.Label(image_type_frame, text="Image Type:").pack(side="left")
        self.image_type_var = StringVar()
        self.image_type_var.set("png")
        image_types = ["png", "svg", "webp"]
        self.image_type_menu = tb.OptionMenu(
            image_type_frame, self.image_type_var, *image_types, bootstyle="info"
            # width=10,  # Removed unsupported 'width' option
        )
        self.image_type_menu.pack(side="left", padx=10)

        # Transformation Specific Options
        self.transformation_options = {}

        # Sort by Frame Number (only for Images to GIF)
        self.sort_check = tb.Checkbutton(
            self.options_frame,
            text="Sort Images by Frame Number",
            variable=self.sort_var,
            bootstyle="primary",
        )
        self.transformation_options["Images to GIF"] = [self.sort_check]
        # Set default state
        # self.sort_check.pack(anchor="w")
        self.sort_check.pack_forget()  # Initially hide; will show if operation is Images to GIF

        # Conversion Buttons
        button_frame = tb.Frame(self.main_frame)
        button_frame.pack(pady=20)

        self.select_input_btn = tb.Button(
            button_frame, text="Select Input", command=self.select_input, bootstyle="info-outline", width=15
        )
        self.select_input_btn.grid(row=0, column=0, padx=10, pady=5)

        self.select_output_btn = tb.Button(
            button_frame, text="Select Output", command=self.select_output, bootstyle="success-outline", width=15
        )
        self.select_output_btn.grid(row=0, column=1, padx=10, pady=5)

        self.start_btn = tb.Button(
            button_frame, text="Start Conversion", command=self.start_conversion, bootstyle="primary", width=20
        )
        self.start_btn.grid(row=0, column=2, padx=10, pady=5)

        # Selected Files
        selected_frame = tb.Frame(self.main_frame)
        selected_frame.pack(fill="x", pady=10)

        tb.Label(selected_frame, text="Input:").grid(row=0, column=0, sticky="w")
        self.input_path_var = StringVar()
        self.input_entry = tb.Entry(
            selected_frame,
            textvariable=self.input_path_var,
            width=80,
        )
        self.input_entry.grid(row=0, column=1, padx=5, pady=2)

        tb.Label(selected_frame, text="Output:").grid(row=1, column=0, sticky="w")
        self.output_path_var = StringVar()
        self.output_entry = tb.Entry(
            selected_frame,
            textvariable=self.output_path_var,
            width=80,
        )
        self.output_entry.grid(row=1, column=1, padx=5, pady=2)

    def toggle_theme(self):
        try:
            if self.style.theme.name == "darkly":
                self.style.theme_use("litera")  # Light theme
                self.theme_toggle.config(text="Dark Mode")
            else:
                self.style.theme_use("darkly")  # Dark theme
                self.theme_toggle.config(text="Light Mode")
        except Exception as e:
            logger.error(f"Error toggling theme: {e}")
            messagebox.showerror("Error", f"Failed to toggle theme: {e}")

    def toggle_ratio_lock(self):
        try:
            if self.ratio_lock_var.get():
                # Calculate and store the current ratio
                width = self.width_slider.get()
                height = self.height_slider.get()
                if height != 0:
                    self.original_ratio = width / height
            else:
                self.original_ratio = 1.0  # Reset ratio
        except Exception as e:
            logger.error(f"Error toggling aspect ratio lock: {e}")
            messagebox.showerror("Error", f"Failed to toggle aspect ratio lock: {e}")

    def update_options(self, selected_operation):
        try:
            # Hide all transformation-specific options
            for widgets in self.transformation_options.values():
                for widget in widgets:
                    widget.pack_forget()

            # Show relevant options based on the selected operation
            if selected_operation in self.transformation_options:
                for widget in self.transformation_options[selected_operation]:
                    widget.pack(anchor="w", pady=2)
            else:
                # Hide sort_check if not applicable
                self.sort_check.pack_forget()

            # Adjust visibility of sort_check based on operation
            if selected_operation == "Images to GIF":
                self.sort_check.pack(anchor="w")
            else:
                self.sort_check.pack_forget()
        except Exception as e:
            logger.error(f"Error updating options: {e}")
            messagebox.showerror("Error", f"Failed to update options: {e}")

    def update_fps_slider(self, event):
        try:
            value = int(self.fps_entry.get())
            value = max(1, min(60, value))
            self.fps_slider.set(value)
        except ValueError:
            logger.warning("Invalid FPS value entered.")
            pass
        except Exception as e:
            logger.error(f"Error updating FPS slider: {e}")
            messagebox.showerror("Error", f"Failed to update FPS slider: {e}")

    def on_fps_slider_change(self, val):
        try:
            self.fps_entry.delete(0, "end")
            self.fps_entry.insert(0, str(int(float(val))))
        except Exception as e:
            logger.error(f"Error in on_fps_slider_change: {e}")

    def update_width_slider(self, event):
        try:
            value = int(self.width_entry.get())
            value = max(128, min(config.get("max_width", 1920), value))
            value = self.snap_to_eight(value)
            if self.ratio_lock_var.get():
                # Adjust height based on ratio
                height = int(value / self.original_ratio)
                height = self.snap_to_eight(height)
                self.height_slider.set(height)
                self.height_entry.delete(0, "end")
                self.height_entry.insert(0, str(height))
            self.width_slider.set(value)
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(value))
        except ValueError:
            logger.warning("Invalid width value entered.")
            pass
        except Exception as e:
            logger.error(f"Error updating width slider: {e}")
            messagebox.showerror("Error", f"Failed to update width slider: {e}")

    def update_height_slider(self, event):
        try:
            value = int(self.height_entry.get())
            value = max(128, min(config.get("max_height", 1032), value))
            value = self.snap_to_eight(value)
            if self.ratio_lock_var.get():
                # Adjust width based on ratio
                width = int(value * self.original_ratio)
                width = self.snap_to_eight(width)
                self.width_slider.set(width)
                self.width_entry.delete(0, "end")
                self.width_entry.insert(0, str(width))
            self.height_slider.set(value)
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(value))
        except ValueError:
            logger.warning("Invalid height value entered.")
            pass
        except Exception as e:
            logger.error(f"Error updating height slider: {e}")
            messagebox.showerror("Error", f"Failed to update height slider: {e}")

    def update_quality_slider(self, event):
        try:
            value = int(self.quality_entry.get())
            value = max(1, min(100, value))
            self.quality_slider.set(value)
        except ValueError:
            logger.warning("Invalid quality value entered.")
            pass
        except Exception as e:
            logger.error(f"Error updating quality slider: {e}")
            messagebox.showerror("Error", f"Failed to update quality slider: {e}")

    def on_width_change(self, val):
        try:
            val = int(float(val))
            snapped_val = self.snap_to_eight(val)
            if snapped_val != val:
                self.width_slider.set(snapped_val)
            if self.ratio_lock_var.get():
                height = int(snapped_val / self.original_ratio)
                height = self.snap_to_eight(height)
                self.height_slider.set(height)
                self.height_entry.delete(0, "end")
                self.height_entry.insert(0, str(height))
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(snapped_val))
        except Exception as e:
            logger.error(f"Error in on_width_change: {e}")

    def on_height_change(self, val):
        try:
            val = int(float(val))
            snapped_val = self.snap_to_eight(val)
            if snapped_val != val:
                self.height_slider.set(snapped_val)
            if self.ratio_lock_var.get():
                width = int(snapped_val * self.original_ratio)
                width = self.snap_to_eight(width)
                self.width_slider.set(width)
                self.width_entry.delete(0, "end")
                self.width_entry.insert(0, str(width))
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(snapped_val))
        except Exception as e:
            logger.error(f"Error in on_height_change: {e}")

    def snap_to_eight(self, value):
        return value - (value % 8)

    def select_input(self):
        try:
            operation = self.operation_var.get()
            if operation in ["Video to GIF", "GIF to Video", "GIF to Images", "Video to Images", "Images to Video"]:
                filetypes = [
                    ("Video Files", "*.mp4;*.avi;*.mov;*.mkv"),
                    ("GIF Files", "*.gif"),
                ]
                path = filedialog.askopenfilename(
                    title="Select Input File", filetypes=filetypes
                )
            elif operation == "Images to GIF":
                path = filedialog.askdirectory(title="Select Input Directory with Images")
            else:
                path = None

            if path:
                self.input_path_var.set(path)
                # Optionally, read media properties if applicable
                if operation in ["Video to GIF", "GIF to Video", "Video to Images", "Images to Video"]:
                    self.read_media_properties(path)
        except Exception as e:
            logger.error(f"Error selecting input: {e}")
            messagebox.showerror("Error", f"Failed to select input: {e}")

    def select_output(self):
        try:
            operation = self.operation_var.get()
            if operation in ["Video to GIF", "GIF to Video", "Images to GIF", "Video to Images", "Images to Video"]:
                if operation == "Images to GIF":
                    output_file = filedialog.asksaveasfilename(
                        defaultextension=".gif",
                        filetypes=[("GIF Files", "*.gif")],
                        title="Save GIF As",
                    )
                elif operation in ["GIF to Video", "Video to Images", "Images to Video"]:
                    # For operations that produce video or images, use appropriate file types
                    if operation == "Images to Video":
                        # Typically produces .mp4 or similar
                        output_file = filedialog.asksaveasfilename(
                            defaultextension=".mp4",
                            filetypes=[("MP4 Files", "*.mp4"), ("AVI Files", "*.avi")],
                            title="Save Video As",
                        )
                    else:
                        # GIF to Video
                        output_file = filedialog.asksaveasfilename(
                            defaultextension=".mp4",
                            filetypes=[("MP4 Files", "*.mp4")],
                            title="Save Video As",
                        )
                else:
                    output_file = filedialog.asksaveasfilename(
                        defaultextension=".gif",
                        filetypes=[("GIF Files", "*.gif")],
                        title="Save GIF As",
                    )
            elif operation == "GIF to Images":
                output_file = filedialog.askdirectory(
                    title="Select Output Directory for Frames"
                )
            else:
                output_file = None

            if output_file:
                self.output_path_var.set(output_file)
        except Exception as e:
            logger.error(f"Error selecting output: {e}")
            messagebox.showerror("Error", f"Failed to select output: {e}")

    def read_media_properties(self, file_path):
        # Use ffprobe to get width, height, and fps
        cmd = [
            FFPROBE_PATH,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-of",
            "json",
            file_path,
        ]
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
            info = json.loads(result.stdout)
            stream = info["streams"][0]
            width = stream.get("width", 512)
            height = stream.get("height", 512)
            fps_str = stream.get("r_frame_rate", "10/1")
            fps = eval(fps_str) if "/" in fps_str else float(fps_str)
            self.original_ratio = width / height if height != 0 else 1.0

            self.width_slider.set(self.snap_to_eight(width))
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(self.snap_to_eight(width)))

            self.height_slider.set(self.snap_to_eight(height))
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(self.snap_to_eight(height)))

            self.fps_slider.set(int(fps))
            self.fps_entry.delete(0, "end")
            self.fps_entry.insert(0, str(int(fps)))

            if self.ratio_lock_var.get():
                self.toggle_ratio_lock()
        except Exception as e:
            logger.error(f"Failed to read media properties: {e}")
            messagebox.showerror("Error", f"Failed to read media properties: {e}")

    def start_conversion(self):
        try:
            operation = self.operation_var.get()
            input_path = self.input_path_var.get()
            output_path = self.output_path_var.get()

            if not input_path or not output_path:
                messagebox.showerror("Error", "Please select both input and output paths.")
                return

            fps = self.fps_slider.get()
            width = self.width_slider.get()
            height = self.height_slider.get()
            quality = self.quality_slider.get()
            image_type = self.image_type_var.get()

            sort_images = self.sort_var.get() if operation == "Images to GIF" else False

            # Additional FFmpeg Options
            codec = "libx264"  # Example option
            bitrate = "1000k"  # Example option

            cmd = []
            message = ""

            if operation == "Video to GIF":
                cmd = [
                    FFMPEG_PATH,
                    "-i",
                    input_path,
                    "-vf",
                    f"fps={fps},scale={width}:{height}:flags=lanczos",
                    "-gifflags",
                    "+transdiff",
                    "-y",
                    output_path,
                ]
                message = "Converting Video to GIF..."
            elif operation == "GIF to Video":
                cmd = [
                    FFMPEG_PATH,
                    "-f",
                    "gif",
                    "-i",
                    input_path,
                    "-movflags",
                    "faststart",
                    "-pix_fmt",
                    "yuv420p",
                    "-vf",
                    f"scale={width}:{height}",
                    "-c:v",
                    codec,
                    "-b:v",
                    bitrate,
                    "-y",
                    output_path,
                ]
                message = "Converting GIF to Video..."
            elif operation == "Images to GIF":
                # Gather images
                supported_ext = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
                images = sorted(
                    [
                        os.path.join(input_path, img)
                        for img in os.listdir(input_path)
                        if img.lower().endswith(supported_ext)
                    ]
                )
                if sort_images:
                    try:
                        images.sort(
                            key=lambda x: int(
                                "".join(filter(str.isdigit, os.path.basename(x))) or 0
                            )
                        )
                    except ValueError:
                        messagebox.showwarning("Warning", "Some images do not have frame numbers. Sorting may be incorrect.")
                temp_txt = os.path.join(config["output_path"], "images_to_gif.txt")
                try:
                    with open(temp_txt, "w") as f:
                        for img in images:
                            f.write(f"file '{img}'\n")
                            f.write(f"duration {1/fps}\n")
                    cmd = [
                        FFMPEG_PATH,
                        "-f",
                        "concat",
                        "-safe",
                        "0",
                        "-i",
                        temp_txt,
                        "-vf",
                        f"scale={width}:{height}:flags=lanczos",
                        "-y",
                        output_path,
                    ]
                    message = "Creating GIF from Images..."
                except Exception as e:
                    logger.error(f"Failed to prepare image list: {e}")
                    messagebox.showerror("Error", f"Failed to prepare image list: {e}")
                    return
            elif operation == "GIF to Images":
                cmd = [
                    FFMPEG_PATH,
                    "-i",
                    input_path,
                    "-vf",
                    f"fps={fps}",
                    os.path.join(output_path, f"frame_%04d.{image_type}"),
                ]
                message = "Extracting Frames from GIF..."
            elif operation == "Video to Images":
                cmd = [
                    FFMPEG_PATH,
                    "-i",
                    input_path,
                    "-vf",
                    f"fps={fps}",
                    os.path.join(output_path, f"frame_%04d.{image_type}"),
                ]
                message = "Extracting Frames from Video..."
            elif operation == "Images to Video":
                # Gather images
                supported_ext = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
                images = sorted(
                    [
                        os.path.join(input_path, img)
                        for img in os.listdir(input_path)
                        if img.lower().endswith(supported_ext)
                    ]
                )
                if sort_images:
                    try:
                        images.sort(
                            key=lambda x: int(
                                "".join(filter(str.isdigit, os.path.basename(x))) or 0
                            )
                        )
                    except ValueError:
                        messagebox.showwarning("Warning", "Some images do not have frame numbers. Sorting may be incorrect.")
                temp_txt = os.path.join(config["output_path"], "images_to_video.txt")
                try:
                    with open(temp_txt, "w") as f:
                        for img in images:
                            f.write(f"file '{img}'\n")
                            f.write(f"duration {1/fps}\n")
                    cmd = [
                        FFMPEG_PATH,
                        "-f",
                        "concat",
                        "-safe",
                        "0",
                        "-i",
                        temp_txt,
                        "-vf",
                        f"scale={width}:{height}:flags=lanczos",
                        "-c:v",
                        codec,
                        "-b:v",
                        bitrate,
                        "-pix_fmt",
                        "yuv420p",
                        "-y",
                        output_path,
                    ]
                    message = "Creating Video from Images..."
                except Exception as e:
                    logger.error(f"Failed to prepare image list: {e}")
                    messagebox.showerror("Error", f"Failed to prepare image list: {e}")
                    return
            else:
                messagebox.showerror("Error", "Unsupported operation selected.")
                return

            threading.Thread(target=self.run_ffmpeg_command, args=(cmd, message)).start()
        except:
            pass

    def run_ffmpeg_command(self, cmd, message):
        try:
            self.show_progress(message)
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            messagebox.showinfo("Success", f"{message} Completed successfully.")
            logger.info(f"{message} Completed successfully.")
            self.open_output_directory()
        except subprocess.CalledProcessError as e:
            logger.error(f"{message} Failed: {e.stderr.decode()}")
            messagebox.showerror("Error", f"{message} Failed.\n{e.stderr.decode()}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, "progress_window") and self.progress_window.winfo_exists():
                self.progress_window.destroy()

    def show_progress(self, message):
        try:
            self.progress_window = tb.Toplevel(self.master)
            self.progress_window.title("Processing")
            self.progress_window.geometry("400x100")
            self.progress_window.resizable(False, False)
            self.progress_window.configure(bg="#2e2e2e")
            tb.Label(
                self.progress_window,
                text=message,
                bootstyle="info",
                font=("Helvetica", 12),
            ).pack(pady=10)
            self.progress_bar = tb.Progressbar(
                self.progress_window, mode="indeterminate", bootstyle="info"
            )
            self.progress_bar.pack(pady=10, padx=20, fill="x")
            self.progress_bar.start()
        except Exception as e:
            logger.error(f"Error showing progress window: {e}")
            messagebox.showerror("Error", f"Failed to show progress window: {e}")

    def open_output_directory(self):
        try:
            output_path = self.output_path_var.get()
            if os.path.isdir(output_path):
                if platform.system() == "Windows":
                    os.startfile(output_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", output_path])
                else:  # Linux and others
                    subprocess.Popen(["xdg-open", output_path])
            elif os.path.isfile(output_path):
                directory = os.path.dirname(output_path)
                self.open_specific_directory(directory)
        except Exception as e:
            logger.error(f"Error opening output directory: {e}")
            messagebox.showerror("Error", f"Failed to open output directory: {e}")

    def open_specific_directory(self, directory):
        try:
            if platform.system() == "Windows":
                os.startfile(directory)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", directory])
            else:  # Linux and others
                subprocess.Popen(["xdg-open", directory])
        except Exception as e:
            logger.error(f"Error opening specific directory: {e}")
            messagebox.showerror("Error", f"Failed to open directory: {e}")


def main():
    try:
        root = tb.Window()
        app = FFmpegApp(root)
        root.mainloop()
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        messagebox.showerror("Critical Error", f"An unhandled exception occurred: {e}")


if __name__ == "__main__":
    main()
