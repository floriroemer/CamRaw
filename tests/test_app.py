"""
Basic integration tests for CamRaw application.
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from camraw import CameraApp


class TestCameraApp:
    """Test the main CameraApp class."""
    
    def test_app_initialization(self):
        """Test basic app initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            app = CameraApp(
                config_path=str(Path(temp_dir) / "config.yaml"),
                output_dir=str(Path(temp_dir) / "captures"),
                debug=True,
                headless=True
            )
            
            assert app.debug is True
            assert app.headless is True
            assert app.output_dir == Path(temp_dir) / "captures"
            assert app.config_manager is not None
            assert app.camera_manager is not None
            assert app.ui is None  # Should be None in headless mode
    
    def test_app_with_gui(self):
        """Test app initialization with GUI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            app = CameraApp(
                config_path=str(Path(temp_dir) / "config.yaml"),
                output_dir=str(Path(temp_dir) / "captures"),
                debug=True,
                headless=False
            )
            
            assert app.headless is False
            assert app.ui is not None
    
    def test_app_cleanup(self):
        """Test app cleanup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            app = CameraApp(
                config_path=str(Path(temp_dir) / "config.yaml"),
                output_dir=str(Path(temp_dir) / "captures"),
                headless=True
            )
            
            # Should not raise any exceptions
            app.cleanup()