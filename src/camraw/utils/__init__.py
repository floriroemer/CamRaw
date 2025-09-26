"""
Utility functions for CamRaw.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(debug: bool = False, log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        debug: Enable debug logging
        log_file: Optional log file path
    """
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if requested
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    logging.info(f"Logging initialized (level: {log_level})")


def ensure_directory(path: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure exists
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        raise


def generate_filename(format_str: str = "IMG_%Y%m%d_%H%M%S", extension: str = "jpg") -> str:
    """
    Generate filename based on format string and current time.
    
    Args:
        format_str: Filename format string (strftime format)
        extension: File extension
        
    Returns:
        Generated filename
    """
    timestamp = datetime.now()
    base_name = timestamp.strftime(format_str)
    return f"{base_name}.{extension}"


def get_file_size_mb(path: Path) -> float:
    """
    Get file size in megabytes.
    
    Args:
        path: File path
        
    Returns:
        File size in MB
    """
    if not path.exists():
        return 0.0
    
    return path.stat().st_size / (1024 * 1024)


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        remaining = seconds % 3600
        minutes = int(remaining // 60)
        secs = remaining % 60
        return f"{hours}h {minutes}m {secs:.1f}s"


def validate_image_path(path: Path) -> bool:
    """
    Validate if path is suitable for saving images.
    
    Args:
        path: Image file path
        
    Returns:
        True if path is valid
    """
    try:
        # Check if directory is writable
        parent_dir = path.parent
        if not parent_dir.exists():
            ensure_directory(parent_dir)
        
        # Check if we can write to the directory
        test_file = parent_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
        
        return True
        
    except Exception as e:
        logging.error(f"Invalid image path {path}: {e}")
        return False


def get_available_disk_space(path: Path) -> float:
    """
    Get available disk space in GB for the given path.
    
    Args:
        path: Path to check
        
    Returns:
        Available disk space in GB
    """
    try:
        import shutil
        _, _, free = shutil.disk_usage(path)
        return free / (1024 ** 3)  # Convert to GB
    except Exception as e:
        logging.error(f"Failed to get disk space for {path}: {e}")
        return 0.0


def cleanup_temp_files(temp_dir: Path, max_age_hours: int = 24) -> None:
    """
    Clean up temporary files older than specified age.
    
    Args:
        temp_dir: Temporary directory to clean
        max_age_hours: Maximum age of files to keep in hours
    """
    try:
        import time
        
        if not temp_dir.exists():
            return
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    logging.debug(f"Cleaned up temp file: {file_path}")
                    
    except Exception as e:
        logging.error(f"Failed to cleanup temp files: {e}")