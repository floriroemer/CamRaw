"""
Configuration settings for CamRaw
"""

import os

# Application settings
APP_NAME = "CamRaw"
VERSION = "1.0.0"

# Default camera settings
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_FPS = 30

# Output settings
OUTPUT_DIR = "output"
PHOTOS_DIR = os.path.join(OUTPUT_DIR, "photos")
VIDEOS_DIR = os.path.join(OUTPUT_DIR, "videos")

# File formats
PHOTO_FORMAT = "jpg"
VIDEO_FORMAT = "mp4"
VIDEO_CODEC = "mp4v"

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480

# Threading settings
FRAME_UPDATE_DELAY = 0.033  # ~30 FPS

# Camera detection settings
MAX_CAMERA_INDEX = 10