"""
Utility functions for the CamRaw application
"""

import os
import platform
import cv2


def get_system_info():
    """Get system information"""
    return {
        'system': platform.system(),
        'version': platform.version(),
        'architecture': platform.architecture()[0],
        'python_version': platform.python_version(),
        'opencv_version': cv2.__version__ if 'cv2' in globals() else 'Not installed'
    }


def get_camera_info(camera_index):
    """Get detailed information about a camera"""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return None
    
    info = {
        'index': camera_index,
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': int(cap.get(cv2.CAP_PROP_FPS)),
        'codec': int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    
    cap.release()
    return info


def ensure_directory(path):
    """Ensure a directory exists"""
    os.makedirs(path, exist_ok=True)


def get_supported_formats():
    """Get supported video formats"""
    formats = {
        'video': ['.mp4', '.avi', '.mov', '.mkv'],
        'photo': ['.jpg', '.png', '.bmp', '.tiff']
    }
    return formats


def validate_camera_access():
    """Validate camera access permissions"""
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret
        return False
    except Exception:
        return False