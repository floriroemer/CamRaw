# CamRaw 📷

<img width="120" height="120" alt="CamRaw Logo" src="assets/Logo.png" />

A simple, cross-platform camera application built with Python that allows you to take photos and record videos with camera selection capabilities.

## Features

- 📸 **Take Photos**: Capture high-quality photos with a single click
- 🎥 **Record Videos**: Start and stop video recording easily
- 🎯 **Camera Selection**: Choose from multiple available cameras
- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 📁 **Organized Output**: Photos and videos are automatically organized in separate folders
- 🎛️ **Simple GUI**: Clean and intuitive interface built with tkinter
- ⚡ **Real-time Preview**: Live camera feed with 30 FPS preview

## Requirements

- Python 3.7 or higher
- OpenCV (opencv-python)
- Pillow (PIL)
- NumPy
- tkinter (usually comes with Python)

## Installation

### Quick Install

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd CamRaw
   ```

2. **Run the installation script**:
   
   **Linux/macOS**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   
   **Windows**:
   ```cmd
   install.bat
   ```

### Manual Install

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

or

```bash
python3 main.py
```

### Using the Application

1. **Select Camera**: Choose your desired camera from the dropdown menu
2. **Start Camera**: Click "Start Camera" to begin the live preview
3. **Take Photos**: Click "Take Photo" to capture and save a photo
4. **Record Videos**: Click "Start Recording" to begin recording, click "Stop Recording" to finish
5. **Stop Camera**: Click "Stop Camera" when done

### Output Files

- **Photos**: Saved in `output/photos/` as `photo_YYYYMMDD_HHMMSS.jpg`
- **Videos**: Saved in `output/videos/` as `video_YYYYMMDD_HHMMSS.mp4`

## Project Structure

```
CamRaw/
├── src/
│   ├── camera_app.py      # Main application code
│   ├── config.py          # Configuration settings
│   └── utils.py           # Utility functions
├── output/
│   ├── photos/            # Captured photos
│   └── videos/            # Recorded videos
├── assets/                # Application assets
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── install.sh            # Linux/macOS installation script
├── install.bat           # Windows installation script
└── README.md             # This file
```

## Supported Platforms

- **Windows 10/11**
- **Linux** (Ubuntu, Fedora, etc.)
- **macOS** (10.14+)

## Camera Permissions

Make sure your system allows camera access for Python applications:

- **Windows**: Check Privacy settings → Camera
- **macOS**: System Preferences → Security & Privacy → Camera
- **Linux**: Usually works out of the box, but check if your user is in the `video` group

## Troubleshooting

### Common Issues

1. **No cameras detected**:
   - Check camera permissions
   - Ensure camera is not being used by another application
   - Try refreshing cameras with the "Refresh Cameras" button

2. **OpenCV installation issues**:
   - Try: `pip install opencv-python --upgrade`
   - On Linux, you might need: `sudo apt-get install python3-opencv`

3. **Video recording not working**:
   - Ensure you have write permissions in the output directory
   - Check available disk space

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify camera permissions on your system
3. Make sure no other applications are using the camera

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve CamRaw!

## License

See the LICENSE file for details.
