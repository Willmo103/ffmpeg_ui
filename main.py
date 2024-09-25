# main_app.py

import os
import json
import shutil
import subprocess
import logging
import logging.config
from pathlib import Path
from tkinter import (
    Tk,
    Frame,
    Label,
    Button,
    Checkbutton,
    IntVar,
    filedialog,
    messagebox,
    Scale,
    HORIZONTAL,
    OptionMenu,
    StringVar,
    ttk,
    Toplevel,
    Entry,
)
from PIL import Image, ImageTk
import threading

# Configuration and Logging Setup
CONFIG_PATH = "conf.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Move conf.example.json to conf.example.json
        shutil.copy("conf.example.json", "conf.json")
        # Load the copied file
        with open("conf.json") as j:
            return json.load(j)
    else:
        with open(CONFIG_PATH, "r") as f:
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
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")

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
        master.geometry("900x700")  # Increased size for more controls
        master.configure(bg="#2e2e2e")  # Dark background for contrast

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Define custom colors
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure(
            "TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 12)
        )
        self.style.configure(
            "TButton",
            foreground="#ffffff",
            background="#4a90e2",
            font=("Helvetica", 12),
        )
        self.style.map("TButton", background=[("active", "#357ab8")])
        self.style.configure("TScale", background="#2e2e2e")
        self.style.configure("TCheckbutton", background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TEntry", fieldbackground="#4a4a4a", foreground="#ffffff")

        # Main Frame
        self.main_frame = Frame(master)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Conversion and Transformation Options
        self.init_main_controls()

    def init_main_controls(self):
        # Operation Selection
        operation_frame = Frame(self.main_frame)
        operation_frame.pack(fill="x", pady=10)

        Label(
            operation_frame, text="Select Operation:", font=("Helvetica", 14, "bold")
        ).pack(anchor="w")

        self.operation_var = StringVar()
        self.operation_var.set("Video to GIF")
        operations = ["Video to GIF", "GIF to Video", "Images to GIF", "GIF to Images"]
        self.operation_menu = OptionMenu(
            operation_frame,
            self.operation_var,
            *operations,
            command=self.update_options,
        )
        self.operation_menu.config(width=20, font=("Helvetica", 12))
        self.operation_menu.pack(anchor="w", pady=5)

        # Dynamic Options Frame
        self.options_frame = Frame(self.main_frame, bg="#2e2e2e")
        self.options_frame.pack(fill="both", pady=10)

        # Common Options
        # Frames Per Second
        fps_frame = Frame(self.options_frame, bg="#2e2e2e")
        fps_frame.pack(fill="x", pady=5)
        Label(fps_frame, text="Frames Per Second (FPS):").pack(side="left")
        self.fps_slider = Scale(
            fps_frame, from_=1, to=60, orient=HORIZONTAL, length=200
        )
        self.fps_slider.set(10)
        self.fps_slider.pack(side="left", padx=10)
        self.fps_entry = Entry(fps_frame, width=5, bg="#4a4a4a", fg="#ffffff")
        self.fps_entry.insert(0, "10")
        self.fps_entry.pack(side="left")
        self.fps_entry.bind("<Return>", self.update_fps_slider)

        # Width and Height
        size_frame = Frame(self.options_frame, bg="#2e2e2e")
        size_frame.pack(fill="x", pady=5)

        Label(size_frame, text="Width:").grid(row=0, column=0, sticky="w")
        self.width_slider = Scale(
            size_frame,
            from_=128,
            to=1920,
            orient=HORIZONTAL,
            length=300,
            command=self.on_width_change,
        )
        self.width_slider.set(512)
        self.width_slider.grid(row=0, column=1, padx=10)
        self.width_entry = Entry(size_frame, width=5, bg="#4a4a4a", fg="#ffffff")
        self.width_entry.insert(0, "512")
        self.width_entry.grid(row=0, column=2)
        self.width_entry.bind("<Return>", self.update_width_slider)

        Label(size_frame, text="Height:").grid(row=1, column=0, sticky="w")
        self.height_slider = Scale(
            size_frame,
            from_=128,
            to=1080,
            orient=HORIZONTAL,
            length=300,
            command=self.on_height_change,
        )
        self.height_slider.set(512)
        self.height_slider.grid(row=1, column=1, padx=10)
        self.height_entry = Entry(size_frame, width=5, bg="#4a4a4a", fg="#ffffff")
        self.height_entry.insert(0, "512")
        self.height_entry.grid(row=1, column=2)
        self.height_entry.bind("<Return>", self.update_height_slider)

        # Quality Slider
        quality_frame = Frame(self.options_frame, bg="#2e2e2e")
        quality_frame.pack(fill="x", pady=5)
        Label(quality_frame, text="Quality:").pack(side="left")
        self.quality_slider = Scale(
            quality_frame, from_=1, to=100, orient=HORIZONTAL, length=200
        )
        self.quality_slider.set(75)
        self.quality_slider.pack(side="left", padx=10)
        self.quality_entry = Entry(quality_frame, width=5, bg="#4a4a4a", fg="#ffffff")
        self.quality_entry.insert(0, "75")
        self.quality_entry.pack(side="left")
        self.quality_entry.bind("<Return>", self.update_quality_slider)

        # Image Type Selection
        image_type_frame = Frame(self.options_frame, bg="#2e2e2e")
        image_type_frame.pack(fill="x", pady=5)
        Label(image_type_frame, text="Image Type:").pack(side="left")
        self.image_type_var = StringVar()
        self.image_type_var.set("png")
        image_types = ["png", "svg", "webp"]
        self.image_type_menu = OptionMenu(
            image_type_frame, self.image_type_var, *image_types
        )
        self.image_type_menu.config(width=10, font=("Helvetica", 12))
        self.image_type_menu.pack(side="left", padx=10)

        # Transformation Specific Options
        self.transformation_options = {}

        # Example: If converting images to GIF, allow sorting options
        self.sort_var = IntVar()
        self.sort_check = Checkbutton(
            self.options_frame,
            text="Sort Images by Frame Number",
            variable=self.sort_var,
            bg="#2e2e2e",
            fg="#ffffff",
        )
        self.transformation_options["Images to GIF"] = [self.sort_check]
        self.sort_check.pack(anchor="w")

        # Conversion Buttons
        button_frame = Frame(self.main_frame, bg="#2e2e2e")
        button_frame.pack(pady=20)

        self.select_input_btn = Button(
            button_frame, text="Select Input", command=self.select_input
        )
        self.select_input_btn.grid(row=0, column=0, padx=10, pady=5)

        self.select_output_btn = Button(
            button_frame, text="Select Output", command=self.select_output
        )
        self.select_output_btn.grid(row=0, column=1, padx=10, pady=5)

        self.start_btn = Button(
            button_frame, text="Start Conversion", command=self.start_conversion
        )
        self.start_btn.grid(row=0, column=2, padx=10, pady=5)

        # Selected Files
        selected_frame = Frame(self.main_frame, bg="#2e2e2e")
        selected_frame.pack(fill="x", pady=10)

        Label(selected_frame, text="Input:").grid(row=0, column=0, sticky="w")
        self.input_path_var = StringVar()
        self.input_entry = Entry(
            selected_frame,
            textvariable=self.input_path_var,
            width=80,
            bg="#4a4a4a",
            fg="#ffffff",
        )
        self.input_entry.grid(row=0, column=1, padx=5, pady=2)

        Label(selected_frame, text="Output:").grid(row=1, column=0, sticky="w")
        self.output_path_var = StringVar()
        self.output_entry = Entry(
            selected_frame,
            textvariable=self.output_path_var,
            width=80,
            bg="#4a4a4a",
            fg="#ffffff",
        )
        self.output_entry.grid(row=1, column=1, padx=5, pady=2)

    def update_options(self, selected_operation):
        # Hide all transformation-specific options
        for widgets in self.transformation_options.values():
            for widget in widgets:
                widget.pack_forget()

        # Show relevant options based on the selected operation
        if selected_operation in self.transformation_options:
            for widget in self.transformation_options[selected_operation]:
                widget.pack(anchor="w", pady=2)

    def update_fps_slider(self, event):
        try:
            value = int(self.fps_entry.get())
            value = max(1, min(60, value))
            self.fps_slider.set(value)
        except ValueError:
            pass

    def update_width_slider(self, event):
        try:
            value = int(self.width_entry.get())
            value = max(128, min(1920, value))
            value = self.snap_to_eight(value)
            self.width_slider.set(value)
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(value))
        except ValueError:
            pass

    def update_height_slider(self, event):
        try:
            value = int(self.height_entry.get())
            value = max(128, min(1080, value))
            value = self.snap_to_eight(value)
            self.height_slider.set(value)
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(value))
        except ValueError:
            pass

    def update_quality_slider(self, event):
        try:
            value = int(self.quality_entry.get())
            value = max(1, min(100, value))
            self.quality_slider.set(value)
        except ValueError:
            pass

    def on_width_change(self, val):
        val = int(float(val))
        snapped_val = self.snap_to_eight(val)
        if snapped_val != val:
            self.width_slider.set(snapped_val)
        self.width_entry.delete(0, "end")
        self.width_entry.insert(0, str(snapped_val))

    def on_height_change(self, val):
        val = int(float(val))
        snapped_val = self.snap_to_eight(val)
        if snapped_val != val:
            self.height_slider.set(snapped_val)
        self.height_entry.delete(0, "end")
        self.height_entry.insert(0, str(snapped_val))

    def snap_to_eight(self, value):
        return value - (value % 8)

    def select_input(self):
        operation = self.operation_var.get()
        if operation in ["Video to GIF", "GIF to Video", "GIF to Images"]:
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
            # Optionally, read video properties if applicable
            if operation in ["Video to GIF", "GIF to Video"]:
                self.read_media_properties(path)

    def select_output(self):
        operation = self.operation_var.get()
        if operation in ["Video to GIF", "GIF to Video", "Images to GIF"]:
            if operation == "Images to GIF":
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".gif",
                    filetypes=[("GIF Files", "*.gif")],
                    title="Save GIF As",
                )
            elif operation == "GIF to Video":
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

    def read_media_properties(self, file_path):
        # Use ffprobe to get width, height, and fps
        cmd = [
            os.path.join(os.path.dirname(FFMPEG_PATH), "ffprobe.exe"),
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
            self.width_slider.set(self.snap_to_eight(width))
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(self.snap_to_eight(width)))

            self.height_slider.set(self.snap_to_eight(height))
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(self.snap_to_eight(height)))

            self.fps_slider.set(int(fps))
            self.fps_entry.delete(0, "end")
            self.fps_entry.insert(0, str(int(fps)))

        except Exception as e:
            logger.error(f"Failed to read media properties: {e}")
            messagebox.showerror("Error", f"Failed to read media properties: {e}")

    def start_conversion(self):
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
                images.sort(
                    key=lambda x: int(
                        "".join(filter(str.isdigit, os.path.basename(x))) or 0
                    )
                )
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
        else:
            messagebox.showerror("Error", "Unsupported operation selected.")
            return

        threading.Thread(target=self.run_ffmpeg_command, args=(cmd, message)).start()

    def run_ffmpeg_command(self, cmd, message):
        try:
            self.show_progress(message)
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            messagebox.showinfo("Success", f"{message} Completed successfully.")
            logger.info(f"{message} Completed successfully.")
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
        self.progress_window = Toplevel(self.master)
        self.progress_window.title("Processing")
        self.progress_window.geometry("400x100")
        self.progress_window.configure(bg="#2e2e2e")
        Label(
            self.progress_window,
            text=message,
            fg="#ffffff",
            bg="#2e2e2e",
            font=("Helvetica", 12),
        ).pack(pady=10)
        self.progress_bar = ttk.Progressbar(self.progress_window, mode="indeterminate")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.start()


def main():
    root = Tk()
    app = FFmpegApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
