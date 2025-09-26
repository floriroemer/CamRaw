# CamRaw

A simple and intuitive Python camera application for desktop computers, designed to capture high-quality images with raw processing capabilities.

## Features

- 🎥 Real-time camera preview
- 📷 Capture high-resolution images
- 🎛️ Manual camera controls (exposure, ISO, focus)
- 📁 Organized photo management
- 🔧 Raw image processing support
- 💾 Multiple output formats (JPEG, PNG, TIFF)
- 🎨 Basic image filters and adjustments
- ⚡ Lightweight and fast performance

## Requirements

- Python 3.8 or higher
- OpenCV for computer vision operations
- A compatible webcam or camera device

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/floriroemer/CamRaw.git
cd CamRaw
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Using pip (Coming Soon)

```bash
pip install camraw
```

## Quick Start

1. Launch CamRaw:
```bash
python main.py
```

2. Connect your camera device
3. Adjust settings using the control panel
4. Click the capture button to take photos
5. Images are automatically saved to the `captures/` directory

## Project Structure

```
CamRaw/
├── src/
│   └── camraw/
│       ├── __init__.py
│       ├── camera/          # Camera control and capture
│       ├── ui/              # User interface components
│       ├── processing/      # Image processing modules
│       ├── utils/           # Utility functions
│       └── config/          # Configuration management
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── examples/                # Usage examples and tutorials
├── captures/                # Default photo storage
├── requirements.txt         # Python dependencies
├── main.py                  # Application entry point
└── README.md
```

## Configuration

CamRaw uses a configuration file located at `config/settings.yaml` to customize:

- Default camera settings
- Output directory preferences  
- Image quality settings
- UI preferences

## Development

### Setting Up Development Environment

1. Fork the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run tests:
```bash
pytest tests/
```

### Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Usage Examples

### Basic Photo Capture
```python
from camraw import CameraApp

app = CameraApp()
app.start_preview()
app.capture_image("my_photo.jpg")
```

### Advanced Camera Controls
```python
from camraw.camera import Camera

camera = Camera()
camera.set_exposure(100)
camera.set_iso(400)
image = camera.capture()
```

## Supported Camera Formats

- USB Webcams
- Built-in laptop cameras
- Professional USB cameras
- IP cameras (HTTP/RTSP streams)

## Roadmap

- [ ] Video recording capabilities
- [ ] Advanced RAW processing
- [ ] Plugin system for filters
- [ ] Cloud storage integration
- [ ] Mobile companion app
- [ ] Batch processing tools

## Troubleshooting

### Common Issues

**Camera not detected:**
- Ensure camera drivers are installed
- Check that no other application is using the camera
- Verify camera permissions in system settings

**Poor image quality:**
- Adjust lighting conditions
- Check camera lens for dust/smudges
- Modify exposure and ISO settings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community for computer vision tools
- Contributors and testers
- Inspiration from professional camera software

## Support

- 📧 Email: support@camraw.example.com
- 🐛 Issues: [GitHub Issues](https://github.com/floriroemer/CamRaw/issues)
- 📖 Documentation: [Full Documentation](https://camraw.readthedocs.io)

---

Made with ❤️ by [Florian Roemer](https://github.com/floriroemer)
