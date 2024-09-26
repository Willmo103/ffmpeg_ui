# ffmpeg_ui
# build.requirements.txt
```plaintext
Pillow==10.4.0

```

# conf.example.json
```json
{
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
    "gif_dir": "",
    "max_width": 1920,
    "max_height": 1032
}

```

# conf.json
```json
{
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
    "output_path": "C:/Users/willm/Videos/FFout",
    "log_file": "ffmpeg_app.log",
    "mp4_dir": "C:/Users/willm/Videos/FFout/mp4",
    "gif_dir": "C:/Users/willm/Videos/FFout/gif",
    "max_width": 1920,
    "max_height": 1032
}

```

# download_ffmpeg.py
```python
from os import makedirs, remove, walk
from os.path import join, exists, abspath, dirname
import zipfile
import urllib.request
from shutil import move, rmtree

ROOT_DIR = abspath(dirname(__file__))
FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
EXTRACT_DIR = join(
    ROOT_DIR, "ffmpeg_download"
)  # Temporary directory to extract the zip file
FFMPEG_DIR = join(ROOT_DIR, "bin")  # This is where we'll place the binaries

for directory in (EXTRACT_DIR, FFMPEG_DIR):
    if not exists(directory):
        makedirs(directory)


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

```

# ffmpeg_app.log
```log
[INFO] > 2024-09-22 23:50:05 - ffmpeg_app - main:199 - Selected file: D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 None
[DEBUG] > 2024-09-22 23:50:08 - PIL.PngImagePlugin - PngImagePlugin:197 - STREAM b'IHDR' 16 13 None
[DEBUG] > 2024-09-22 23:50:08 - PIL.PngImagePlugin - PngImagePlugin:197 - STREAM b'pHYs' 41 9 None
[DEBUG] > 2024-09-22 23:50:08 - PIL.PngImagePlugin - PngImagePlugin:197 - STREAM b'IDAT' 62 4096 None
[INFO] > 2024-09-22 23:51:53 - ffmpeg_app - main:199 - Selected file: D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 None
[INFO] > 2024-09-23 00:06:06 - ffmpeg_app - main:218 - Selected video file: D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 None
[INFO] > 2024-09-23 00:10:16 - ffmpeg_app - main:218 - Selected video file: D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 None
[INFO] > 2024-09-23 00:10:33 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/FFout/gif\xvideos.com_9573c6403c528017791664ea4a6fe40b.gif None
[INFO] > 2024-09-23 00:10:34 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/FFout/gif\xvideos.com_9573c6403c528017791664ea4a6fe40b.gif None
[INFO] > 2024-09-23 00:10:45 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/FFout/gif\xvideos.com_9573c6403c528017791664ea4a6fe40b.gif None
[INFO] > 2024-09-23 00:32:16 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/bx3di0ft8dvz.gif -movflags faststart -pix_fmt yuv420p -vf scale=320:-1 -y D:/Downloads/WhoreShakes.mp4 None
[ERROR] > 2024-09-23 00:32:17 - ffmpeg_app - main:401 - Converting GIF to Video... Failed. Error: ffmpeg version 7.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-zlib --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-sdl2 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libgme --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libtheora --enable-libvo-amrwbenc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-librubberband
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
Input #0, gif, from 'D:/Downloads/bx3di0ft8dvz.gif':
  Duration: 00:00:21.46, start: 0.000000, bitrate: 5496 kb/s
  Stream #0:0: Video: gif, bgra, 640x353, 11.11 fps, 100 tbr, 100 tbn
Stream mapping:
  Stream #0:0 -> #0:0 (gif (native) -> h264 (libx264))
Press [q] to stop, [?] for help
[libx264 @ 0000015927e65300] height not divisible by 2 (320x177)
[vost#0:0/libx264 @ 0000015927e64f40] Error while opening encoder - maybe incorrect parameters such as bit_rate, rate, width or height.
[vf#0:0 @ 0000015927e5b400] Error sending frames to consumers: Generic error in an external library
[vf#0:0 @ 0000015927e5b400] Task finished with error code: -542398533 (Generic error in an external library)
[vf#0:0 @ 0000015927e5b400] Terminating thread with return code -542398533 (Generic error in an external library)
[vost#0:0/libx264 @ 0000015927e64f40] Could not open encoder before EOF
[vost#0:0/libx264 @ 0000015927e64f40] Task finished with error code: -22 (Invalid argument)
[vost#0:0/libx264 @ 0000015927e64f40] Terminating thread with return code -22 (Invalid argument)
[out#0/mp4 @ 0000015927e64540] Nothing was written into output file, because at least one of its streams received no packets.
frame=    0 fps=0.0 q=0.0 Lsize=       0KiB time=N/A bitrate=N/A dup=9 drop=0 speed=N/A    
Conversion failed!
 None
[INFO] > 2024-09-23 00:33:14 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y D:/Downloads/thai_fucked.gif None
[INFO] > 2024-09-23 00:33:18 - ffmpeg_app - main:398 - Converting Video to GIF... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:41:55 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf scale=1090:720 -c:v libx264 -crf 31 -y D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b__Upgraded.mp4 None
[INFO] > 2024-09-23 00:43:12 - ffmpeg_app - main:398 - Applying Transformation... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:49:55 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b__Upgraded.mp4 -vf scale=1304:720 -c:v libx264 -crf 31 -y D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b__Upgraded_full.mp4 None
[INFO] > 2024-09-23 00:51:24 - ffmpeg_app - main:398 - Applying Transformation... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:53:31 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y D:/Downloads/Thai_Fucked_gif.gif None
[INFO] > 2024-09-23 00:53:35 - ffmpeg_app - main:398 - Converting Video to GIF... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:54:22 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/xvideos.com_9573c6403c528017791664ea4a6fe40b__Upgraded_full.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y D:/Downloads/Thai_Fucked_gif.gif None
[INFO] > 2024-09-23 00:54:31 - ffmpeg_app - main:398 - Converting Video to GIF... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:55:01 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/Thai_Fucked_gif.gif -vf fps=10 D:/Downloads/Phillipino\frame_%04d.png -y None
[INFO] > 2024-09-23 00:55:09 - ffmpeg_app - main:398 - Extracting Frames from GIF... Completed successfully. Output:  None
[INFO] > 2024-09-23 00:59:26 - ffmpeg_app - main:393 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/Thai_Fucked_gif.gif -vf fps=10 D:/Downloads/Phillipino_LG\frame_%04d.png -y None
[INFO] > 2024-09-23 00:59:34 - ffmpeg_app - main:398 - Extracting Frames from GIF... Completed successfully. Output:  None
[INFO] > 2024-09-23 01:19:33 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/Thai_Fucked_gif.gif -vf fps=10 D:/Downloads/Phillipino_LG/2\frame_%04d.png -y None
[INFO] > 2024-09-23 01:19:43 - ffmpeg_app - main:453 - Extracting Frames from GIF... Completed successfully. None
[INFO] > 2024-09-23 02:04:35 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -framerate 10 -i D:/Downloads/ed\frame_%04d.png -vf scale=320:-1:flags=lanczos -y D:/Downloads/ed/ed.gif None
[ERROR] > 2024-09-23 02:04:36 - ffmpeg_app - main:455 - Creating GIF from Images... Failed: ffmpeg version 7.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-zlib --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-sdl2 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libgme --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libtheora --enable-libvo-amrwbenc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-librubberband
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
[image2 @ 000001e8c485fa80] Could find no file with path 'D:/Downloads/ed\frame_%04d.png' and index in the range 0-4
[in#0 @ 000001e8c485f680] Error opening input: No such file or directory
Error opening input file D:/Downloads/ed\frame_%04d.png.
Error opening input files: No such file or directory
 None
[INFO] > 2024-09-23 02:10:46 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -framerate 10 -i D:/Downloads/ed\frame_%04d.png -vf scale=320:-1:flags=lanczos -y D:/Downloads/ed/ed.gif None
[INFO] > 2024-09-23 02:10:48 - ffmpeg_app - main:453 - Creating GIF from Images... Completed successfully. None
[INFO] > 2024-09-23 02:29:57 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i D:/Downloads/bx3di0ft8dvz.gif -vf fps=10 D:/Downloads/floppy\frame_%04d.png -y None
[INFO] > 2024-09-23 02:30:02 - ffmpeg_app - main:453 - Extracting Frames from GIF... Completed successfully. None
[INFO] > 2024-09-23 03:04:54 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -framerate 10 -i B:/Stable_Trainer/Data/floppy_ed1\frame_%04d.png -vf scale=320:-1:flags=lanczos -y B:/Stable_Trainer/Data/floppy_ed1/floppy_ed.gif None
[INFO] > 2024-09-23 03:05:04 - ffmpeg_app - main:453 - Creating GIF from Images... Completed successfully. None
[INFO] > 2024-09-23 18:04:58 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -framerate 10 -i D:/ed_floppy_new\frame_%04d.png -vf scale=320:-1:flags=lanczos -y D:/ed_floppy_new/ed_new_floppy.gif None
[ERROR] > 2024-09-23 18:04:59 - ffmpeg_app - main:455 - Creating GIF from Images... Failed: ffmpeg version 7.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-zlib --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-sdl2 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libgme --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libtheora --enable-libvo-amrwbenc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-librubberband
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
[image2 @ 0000026cc7befa80] Could find no file with path 'D:/ed_floppy_new\frame_%04d.png' and index in the range 0-4
[in#0 @ 0000026cc7bef680] Error opening input: No such file or directory
Error opening input file D:/ed_floppy_new\frame_%04d.png.
Error opening input files: No such file or directory
 None
[INFO] > 2024-09-23 18:12:58 - ffmpeg_app - main:450 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -framerate 10 -i D:/ed_floppy_new\frame_%04d.png -vf scale=320:-1:flags=lanczos -y D:/ed_floppy_new/ed_new_floppy.gif None
[INFO] > 2024-09-23 18:13:00 - ffmpeg_app - main:453 - Creating GIF from Images... Completed successfully. None
[INFO] > 2024-09-24 02:18:11 - ffmpeg_app - main:453 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 -vf fps=10,scale=320:-1:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/young_puss.gif None
[INFO] > 2024-09-24 02:18:15 - ffmpeg_app - main:456 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 02:21:26 - ffmpeg_app - main:453 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 -vf scale=769:518:flags=lanczos -movflags faststart -pix_fmt yuv420p -y C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 None
[ERROR] > 2024-09-24 02:21:26 - ffmpeg_app - main:458 - Applying Transformation... Failed: ffmpeg version 7.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-zlib --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-sdl2 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libgme --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libtheora --enable-libvo-amrwbenc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-librubberband
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
[mov,mp4,m4a,3gp,3g2,mj2 @ 0000024ebe8848c0] st: 1 edit list: 1 Missing key frame while searching for timestamp: 0
[mov,mp4,m4a,3gp,3g2,mj2 @ 0000024ebe8848c0] st: 1 edit list 1 Cannot find an index entry before timestamp: 0.
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 0
    compatible_brands: mp41avc1
    creation_time   : 2024-09-24T07:16:43.000000Z
    playback_requirements: QuickTime 6.0 or greater
    playback_requirements-eng: QuickTime 6.0 or greater
    encoder         : vlc 3.0.17.4 stream output
    encoder-eng     : vlc 3.0.17.4 stream output
  Duration: 00:00:12.44, start: 0.000000, bitrate: 627 kb/s
  Stream #0:0[0x1](eng): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 128 kb/s (default)
      Metadata:
        creation_time   : 2024-09-24T07:16:43.000000Z
        handler_name    : SoundHandler
        vendor_id       : [0][0][0][0]
  Stream #0:1[0x2](eng): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 854x480, 492 kb/s, 25 fps, 25 tbr, 90k tbn (default)
      Metadata:
        creation_time   : 2024-09-24T07:16:43.000000Z
        handler_name    : VideoHandler
        vendor_id       : [0][0][0][0]
Output C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 same as Input #0 - exiting
FFmpeg cannot edit existing files in-place.
Error opening output file C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4.
Error opening output files: Invalid argument
 None
[INFO] > 2024-09-24 02:49:40 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 -vf fps=25,scale=768:512:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/young_whore.gif None
[INFO] > 2024-09-24 02:49:44 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 02:55:28 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4 -vf fps=16,scale=912:512:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/young_whore.gif None
[INFO] > 2024-09-24 02:55:34 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 02:59:49 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-02h16m30s-vlc-record-2024-09-24-02h15m07s-33.mp4-.mp4-.mp4 -vf fps=20,scale=1024:512:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/young_whore_hq.gif None
[INFO] > 2024-09-24 02:59:53 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 03:02:21 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/young_whore.gif -vf fps=20 C:/Users/willm/Videos/FFout/gif/Young Whore Lng\frame_%04d.png None
[INFO] > 2024-09-24 03:02:35 - ffmpeg_app - main:495 - Extracting Frames from GIF... Completed successfully. None
[INFO] > 2024-09-24 03:10:03 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/vlc-record-2024-09-24-03h08m09s-39.mp4-.mp4 -vf fps=8,scale=1024:512:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/sqrt_jewels.gif None
[INFO] > 2024-09-24 03:10:08 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 03:34:00 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/joa20fwd0.mp4 -vf fps=60,scale=792:512:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/jiggle.gif None
[INFO] > 2024-09-24 03:34:05 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-24 03:37:55 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/joa20fwd0.mp4 -vf fps=60,scale=1280:976:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/jiggle.gif None
[INFO] > 2024-09-24 03:38:02 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-25 01:56:43 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -i C:/Users/willm/Videos/joa20fwd0.mp4 -vf fps=60,scale=864:440:flags=lanczos -gifflags +transdiff -y C:/Users/willm/Videos/jjed.gif None
[INFO] > 2024-09-25 01:56:50 - ffmpeg_app - main:495 - Converting Video to GIF... Completed successfully. None
[INFO] > 2024-09-25 02:02:51 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -f gif -i D:/ed_floppy_new/ed_new_floppy.gif -movflags faststart -pix_fmt yuv420p -vf scale=880:640 -y D:/ed_floppy_new/ed.mp4 None
[INFO] > 2024-09-25 02:02:56 - ffmpeg_app - main:495 - Converting GIF to Video... Completed successfully. None
[INFO] > 2024-09-25 03:00:23 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -f concat -safe 0 -i C:/Users/willm/Videos/FFout\images_to_gif.txt -vf scale=880:640:flags=lanczos -y B:/Stable_Trainer/Data/edjo1/eduffy1/edjo.gif None
[INFO] > 2024-09-25 03:00:32 - ffmpeg_app - main:495 - Creating GIF from Images... Completed successfully. None
[INFO] > 2024-09-25 03:01:46 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -f concat -safe 0 -i C:/Users/willm/Videos/FFout\images_to_gif.txt -vf scale=880:640:flags=lanczos -y B:/Stable_Trainer/Data/edjo1/eduffy1/edjo.gif None
[INFO] > 2024-09-25 03:01:52 - ffmpeg_app - main:495 - Creating GIF from Images... Completed successfully. None
[INFO] > 2024-09-25 03:02:58 - ffmpeg_app - main:492 - Running FFmpeg command: C:\Users\willm\Desktop\ffmpeg_ui\bin\ffmpeg.exe -f concat -safe 0 -i C:/Users/willm/Videos/FFout\images_to_gif.txt -vf scale=920:512:flags=lanczos -y B:/Stable_Trainer/Data/edjo1/eduffy1/edj_o.gif None
[INFO] > 2024-09-25 03:03:05 - ffmpeg_app - main:495 - Creating GIF from Images... Completed successfully. None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:457 - Error in on_fps_slider_change: 'FFmpegApp' object has no attribute 'fps_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_slider' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change:  None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:530 - Error in on_width_change: 'FFmpegApp' object has no attribute 'height_entry' None
[ERROR] > 2024-09-26 10:47:39 - ffmpeg_app - main:547 - Error in on_height_change: 'FFmpegApp' object has no attribute 'height_entry' None
[CRITICAL] > 2024-09-26 10:47:39 - ffmpeg_app - main:927 - Unhandled exception: maximum recursion depth exceeded while calling a Python object None

```

# ffmpeg_app.spec
```python
# ffmpeg_app.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=[
        (os.path.join('bin', 'ffmpeg.exe'), 'bin'),
        (os.path.join('bin', 'ffprobe.exe'), 'bin'),
        (os.path.join('bin', 'ffplay.exe'), 'bin')
    ],
    datas=[
        ('conf.example.json', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ffmpeg_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ffmpeg_app'
)

```

# install.py
```python
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

    required = ["Pillow"]
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

```

# main.py
```python
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

```

# _dev/conf.json
```json
{
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
    "output_path": "C:/Users/willm/Videos/FFout",
    "log_file": "ffmpeg_app.log",
    "mp4_dir": "C:/Users/willm/Videos/FFout/mp4",
    "gif_dir": "C:/Users/willm/Videos/FFout/gif"
}

```

