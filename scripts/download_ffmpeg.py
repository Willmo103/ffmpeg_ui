from os import makedirs, remove, walk
from os.path import join, exists
import zipfile
import urllib.request
from shutil import move, rmtree

FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
EXTRACT_DIR = "ffmpeg_download"  # Temporary directory to extract the zip file
FFMPEG_DIR = "bin"  # This is where we'll place the binaries


def download_ffmpeg():
    # Download the FFmpeg zip file
    print("Downloading FFmpeg...")
    zip_path, _ = urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, "ffmpeg.zip")
    print(f"Downloaded FFmpeg to {zip_path}")

    # Extract the zip file
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # Find the folder that contains ffmpeg.exe, ffprobe.exe, and ffplay.exe
    ffmpeg_subdir = None
    for root, _, files in walk(EXTRACT_DIR):
        if "ffmpeg.exe" in files and "ffprobe.exe" in files:
            ffmpeg_subdir = root
            break

    if not ffmpeg_subdir:
        raise Exception("Failed to find FFmpeg binaries after extraction.")

    # Ensure the ffmpeg_bin directory exists
    if not exists(FFMPEG_DIR):
        makedirs(FFMPEG_DIR)

    # Move the ffmpeg, ffprobe, and ffplay binaries to the target directory
    move(
        join(ffmpeg_subdir, "ffmpeg.exe"),
        join(FFMPEG_DIR, "ffmpeg.exe"),
    )
    move(
        join(ffmpeg_subdir, "ffprobe.exe"),
        join(FFMPEG_DIR, "ffprobe.exe"),
    )
    move(
        join(ffmpeg_subdir, "ffplay.exe"),
        join(FFMPEG_DIR, "ffplay.exe"),
    )

    # Clean up
    remove(zip_path)
    rmtree(EXTRACT_DIR)

    print(f"FFmpeg, FFprobe, and FFplay binaries are now located in {FFMPEG_DIR}")


if __name__ == "__main__":
    download_ffmpeg()
