import logging
from logging.config import dictConfig
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import subprocess
import json

# Set up Global Variables
OUTPUT_PATH: str
LOGGER_NAME: str
LOG_FILE: str

try:
    with open("conf.json", "r") as j:
        data = json.load(j)
    OUTPUT_PATH = data["output_dir"]
    dictConfig(data["logging_config"])
    LOGGER_NAME = data["logger_name"]
    LOG_FILE = os.path.join(os.path.dirname(__file__), data["log_file"])
except FileNotFoundError or FileExistsError as err:
    print(f"Error: {err}")
    exit(1)


# Set up logging
logger = logging.getLogger(LOGGER_NAME)


# Function to get video duration using ffprobe
def get_video_duration():
    input_file = input_file_var.get()
    if not input_file:
        return
    try:
        ffprobe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_file,
        ]
        result = subprocess.run(
            ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        duration = float(result.stdout.decode("utf-8").strip())
        video_duration_label.config(text=f"Video Duration: {int(duration)} seconds")
        start_slider.config(to=int(duration))
        end_slider.config(to=int(duration))
        logger.info(f"Video: {input_file} duration: {int(duration)} seconds")
        return duration
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve video duration: {str(e)}")
        logger.error(f"Failed to retrieve video duration: {str(e)}")
        return 0


# Function to execute ffmpeg trimming command
def process_video():
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    output_filename = rename_var.get()
    start_trim = start_slider.get() if trim_enabled_var.get() else 0
    end_trim = end_slider.get() if trim_enabled_var.get() else 0
    output_format = format_var.get()
    logger.info(
        f"Processing video: {input_file} to {output_folder} as {output_filename}.{output_format}"
    )

    if not input_file or not output_folder or not output_filename:
        messagebox.showerror(
            "Error", "Please select both input file, output folder, and provide a name."
        )
        logger.error(
            "Please select both input file, output folder, and provide a name."
        )
        return

    # Ensure output folders exist
    mp4_folder = os.path.join(output_folder, "mp4")
    gif_folder = os.path.join(output_folder, "gif")
    os.makedirs(mp4_folder, exist_ok=True)
    os.makedirs(gif_folder, exist_ok=True)

    # Construct output file path based on format
    if output_format == "GIF":
        output_path = os.path.join(gif_folder, f"{output_filename}.gif")
        logger.info(f"Output path: {output_path}")
        try:
            ffmpeg_cmd = [
                "ffmpeg",
                "-i",
                input_file,
                "-ss",
                str(start_trim),
                "-t",
                str(video_duration - end_trim),
                "-vf",
                "fps=15,scale=640:-1:flags=lanczos",  # Adjust fps and scale for GIF
                "-y",
                output_path,
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            logger.info(f"GIF saved as {output_filename}.gif")
            messagebox.showinfo("Success", f"GIF saved as {output_filename}.gif")
        except Exception as e:
            logger.error(f"Failed to create GIF: {str(e)}")
            messagebox.showerror("Error", f"Failed to create GIF: {str(e)}")
    else:
        output_path = os.path.join(mp4_folder, f"{output_filename}.mp4")
        try:
            ffmpeg_cmd = [
                "ffmpeg",
                "-i",
                input_file,
                "-ss",
                str(start_trim),
                "-t",
                str(video_duration - end_trim),
                "-y",
                output_path,
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            logger.info(f"Video saved as {output_filename}.mp4")
            messagebox.showinfo("Success", f"Video saved as {output_filename}.mp4")
        except Exception as e:
            logger.error(f"Failed to save MP4: {str(e)}")
            messagebox.showerror("Error", f"Failed to save MP4: {str(e)}")


# Function to open file dialog for selecting input file
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        input_file_var.set(file_path)
        get_video_duration()


# Function to open file dialog for selecting output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)


# Function to toggle trimming options
def toggle_trimming():
    if trim_enabled_var.get():
        start_slider.config(state="normal")
        end_slider.config(state="normal")
    else:
        start_slider.config(state="disabled")
        end_slider.config(state="disabled")


# Create the main window
root = tk.Tk()
root.title("FFmpeg Video Processor")

# Input File Dropdown
input_file_var = tk.StringVar()
input_label = tk.Label(root, text="Input Video:")
input_label.grid(row=0, column=0, padx=10, pady=10)
input_dropdown = tk.Entry(root, textvariable=input_file_var, width=50)
input_dropdown.grid(row=0, column=1, padx=10, pady=10)
input_button = tk.Button(root, text="Browse", command=select_input_file)
input_button.grid(row=0, column=2, padx=10, pady=10)

# Video Duration Label
video_duration_label = tk.Label(root, text="Video Duration: Unknown")
video_duration_label.grid(row=1, column=1, padx=10, pady=10)
video_duration = 0

# Output Folder Dropdown (Hidden by default)
output_folder_var = tk.StringVar()
output_folder_var.set(os.getcwd())  # Default to current working directory
output_label = tk.Label(root, text="Output Folder (Hidden):")
output_dropdown = tk.Entry(root, textvariable=output_folder_var, width=50)
output_button = tk.Button(root, text="Browse", command=select_output_folder)

# Rename field
rename_label = tk.Label(root, text="Rename Output File:")
rename_label.grid(row=2, column=0, padx=10, pady=10)
rename_var = tk.StringVar()
rename_entry = tk.Entry(root, textvariable=rename_var, width=50)
rename_entry.grid(row=2, column=1, padx=10, pady=10)

# Sliders for trimming start and end
start_slider_label = tk.Label(root, text="Trim Seconds from Start:")
start_slider_label.grid(row=3, column=0, padx=10, pady=10)
start_slider = tk.Scale(
    root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, state="disabled"
)
start_slider.grid(row=3, column=1, padx=10, pady=10)

end_slider_label = tk.Label(root, text="Trim Seconds from End:")
end_slider_label.grid(row=4, column=0, padx=10, pady=10)
end_slider = tk.Scale(
    root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, state="disabled"
)
end_slider.grid(row=4, column=1, padx=10, pady=10)

# Radio button to enable/disable trimming
trim_enabled_var = tk.IntVar(value=0)
trim_radio = tk.Checkbutton(
    root, text="Enable Trimming", variable=trim_enabled_var, command=toggle_trimming
)
trim_radio.grid(row=5, column=1, padx=10, pady=10)

# Format Selection (MP4 or GIF)
format_var = tk.StringVar(value="GIF")
format_label = tk.Label(root, text="Output Format:")
format_label.grid(row=6, column=0, padx=10, pady=10)
format_dropdown = tk.OptionMenu(root, format_var, "MP4", "GIF")
format_dropdown.grid(row=6, column=1, padx=10, pady=10)

# Process Button
process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.grid(row=7, column=1, padx=10, pady=10)

# Menu for hiding output folder option
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(
    label="Select Output Folder",
    command=lambda: (output_label.grid(), output_dropdown.grid(), output_button.grid()),
)
menu_bar.add_cascade(label="Options", menu=file_menu)
root.config(menu=menu_bar)

# Run the main loop
root.mainloop()
