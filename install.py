# install.py

import subprocess
import sys
import os

def install_dependencies():
    try:
        import pip
    except ImportError:
        print("pip is not installed. Please install pip first.")
        sys.exit(1)

    required = ['Pillow']
    for package in required:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_ffmpeg():
    # Check if FFmpeg is already downloaded
    ffmpeg_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin")
    if not os.path.exists(ffmpeg_dir):
        subprocess.check_call([sys.executable, "setup_ffmpeg.py"])
    else:
        print("FFmpeg is already installed.")

def main():
    install_dependencies()
    download_ffmpeg()
    print("Installation complete.")

if __name__ == "__main__":
    main()
