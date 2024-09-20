import os
import zipfile
import urllib.request
import shutil

FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "bin"  # This is where we'll place the binaries
EXTRACT_DIR = "ffmpeg_download"  # Temporary directory to extract the zip file


def download_ffmpeg():
    # Download the FFmpeg zip file
    print("Downloading FFmpeg...")
    zip_path, _ = urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, "ffmpeg.zip")
    print(f"Downloaded FFmpeg to {zip_path}")

    # Extract the zip file
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # Find the folder that contains ffmpeg.exe, ffprobe.exe, and ffplay.exe
    ffmpeg_subdir = None
    for root, _, files in os.walk(EXTRACT_DIR):
        if "ffmpeg.exe" in files and "ffprobe.exe" in files:
            ffmpeg_subdir = root
            break

    if not ffmpeg_subdir:
        raise Exception("Failed to find FFmpeg binaries after extraction.")

    # Ensure the ffmpeg_bin directory exists
    if not os.path.exists(FFMPEG_DIR):
        os.makedirs(FFMPEG_DIR)

    # Move the ffmpeg, ffprobe, and ffplay binaries to the target directory
    shutil.move(os.path.join(ffmpeg_subdir, "ffmpeg.exe"), os.path.join(FFMPEG_DIR, "ffmpeg.exe"))
    shutil.move(os.path.join(ffmpeg_subdir, "ffprobe.exe"), os.path.join(FFMPEG_DIR, "ffprobe.exe"))
    shutil.move(os.path.join(ffmpeg_subdir, "ffplay.exe"), os.path.join(FFMPEG_DIR, "ffplay.exe"))

    # Clean up
    os.remove(zip_path)
    shutil.rmtree(EXTRACT_DIR)

    print(f"FFmpeg, FFprobe, and FFplay binaries are now located in {FFMPEG_DIR}")


if __name__ == "__main__":
    download_ffmpeg()
