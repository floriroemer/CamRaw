#!/usr/bin/env python3
"""
CamRaw - Simple Camera Application
A cross-platform camera app for taking photos and videos
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from camera_app import main

if __name__ == "__main__":
    main()