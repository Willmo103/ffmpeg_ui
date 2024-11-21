# FFmpeg UI Application

A modern, user-friendly graphical interface for FFmpeg media conversions and transformations.

## Features

- Convert between different media formats:
  - Video to GIF
  - GIF to Video
  - Images to GIF
  - GIF to Images
  - Video to Images
  - Images to Video
- Customizable settings:
  - Frame rate (FPS)
  - Resolution (width/height)
  - Quality control
  - Aspect ratio locking
  - Image format selection (PNG, SVG, WEBP)
- Dark/Light theme support
- Progress tracking
- Automatic output directory opening
- Smart frame sorting for image sequences
- Multi-platform support (Windows, macOS, Linux)

## Requirements

- Python 3.7+
- FFmpeg (automatically downloaded during setup)
- Dependencies:
  - ttkbootstrap
  - Pillow

## Installation

1. Clone the repository:

   ```bash
   git clone [repository-url]
   cd ffmpeg-ui
   ```

2. Run the installer:

   ```bash
   python install.py
   ```

This will automatically:

- Install required Python packages
- Download and set up FFmpeg

## Usage

1. Launch the application:

   ```bash
   python main.py
   ```

2. Select your desired operation from the dropdown menu

3. Configure your conversion settings:
   - Set frame rate
   - Adjust dimensions
   - Choose quality level
   - Select output format
4. Choose input file(s) or directory
5. Select output location
6. Click "Start Conversion"

## Configuration

The application uses `conf.json` for settings. Default configuration is created on first run, but can be modified for:

- Custom output directories
- Maximum resolution limits
- Logging preferences
- Default paths

## Logging

Logs are stored in `app.log` by default. The logging level and format can be customized in `conf.json`.

## Features in Detail

### Video/GIF Conversion

- Maintains quality while optimizing file size
- Supports multiple video formats
- Configurable frame rates and resolutions

### Image Sequence Handling

- Smart frame number detection
- Automatic sequence sorting
- Multiple image format support

### User Interface

- Modern ttkbootstrap theme
- Intuitive controls
- Real-time preview options
- Progress indication

## Known Limitations

- SVG support is limited to conversion operations
- Maximum resolution is configurable but default-limited to 1920x1032
- Some video codecs may require additional system libraries

## Troubleshooting

1. FFmpeg Missing:
   - Run `python install.py` to reinstall FFmpeg
   - Verify FFmpeg is in the `bin` directory

2. Permission Issues:
   - Ensure write permissions in output directories
   - Run with appropriate privileges

3. Conversion Errors:
   - Check the log file for detailed error messages
   - Verify input file format is supported

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Acknowledgments

- FFmpeg for the underlying conversion engine
- ttkbootstrap for the modern UI elements
- The Python community for various supporting libraries
