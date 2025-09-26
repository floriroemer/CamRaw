"""
Tests for CamRaw camera functionality.
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from camraw.camera import CameraManager, CameraDevice
from camraw.config import ConfigManager


class TestCameraDevice:
    """Test camera device functionality."""
    
    def test_camera_device_creation(self):
        """Test creating a camera device."""
        camera = CameraDevice(0)
        assert camera.device_id == 0
        assert camera.name == "Camera 0"
        assert not camera.is_open
        assert not camera.preview_active
    
    def test_camera_availability(self):
        """Test camera availability check."""
        camera = CameraDevice(0)
        # Should be available (mocked)
        assert camera.is_available()
        
        camera2 = CameraDevice(5)
        # Should not be available (mocked)
        assert not camera2.is_available()
    
    def test_camera_open_close(self):
        """Test opening and closing camera."""
        camera = CameraDevice(0)
        
        # Open camera
        success = camera.open()
        assert success
        assert camera.is_open
        
        # Close camera
        camera.close()
        assert not camera.is_open
        assert not camera.preview_active
    
    def test_camera_settings(self):
        """Test getting and updating camera settings."""
        camera = CameraDevice(0)
        camera.open()
        
        # Get default settings
        settings = camera.get_settings()
        assert "exposure" in settings
        assert "iso" in settings
        assert settings["iso"] == 100
        
        # Update settings
        new_settings = {"iso": 400, "exposure": -10}
        success = camera.update_settings(new_settings)
        assert success
        
        # Verify updated settings
        updated_settings = camera.get_settings()
        assert updated_settings["iso"] == 400
        assert updated_settings["exposure"] == -10
        
        camera.close()
    
    def test_image_capture(self):
        """Test image capture functionality."""
        camera = CameraDevice(0)
        camera.open()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_capture.jpg"
            
            success = camera.capture_image(output_path)
            assert success
            assert output_path.exists()
        
        camera.close()


class TestCameraManager:
    """Test camera manager functionality."""
    
    def test_camera_manager_creation(self):
        """Test creating a camera manager."""
        config = ConfigManager()
        manager = CameraManager(config)
        
        assert manager.config_manager is config
        assert manager.current_camera is None
        assert len(manager.available_cameras) == 0
    
    def test_camera_initialization(self):
        """Test camera manager initialization."""
        config = ConfigManager()
        manager = CameraManager(config)
        
        success = manager.initialize()
        assert success
        assert len(manager.available_cameras) > 0
        assert manager.current_camera is not None
        
        manager.cleanup()
    
    def test_camera_selection(self):
        """Test selecting different cameras."""
        config = ConfigManager()
        manager = CameraManager(config)
        manager.initialize()
        
        # Select camera 0 (should succeed)
        success = manager.select_camera(0)
        assert success
        assert manager.current_camera.device_id == 0
        
        # Select camera 1 (should succeed if available)
        if len(manager.available_cameras) > 1:
            success = manager.select_camera(1)
            assert success
            assert manager.current_camera.device_id == 1
        
        # Select non-existent camera
        success = manager.select_camera(99)
        assert not success
        
        manager.cleanup()
    
    def test_image_capture_through_manager(self):
        """Test image capture through manager."""
        config = ConfigManager()
        manager = CameraManager(config)
        manager.initialize()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "manager_capture.jpg"
            
            success = manager.capture_image(output_path)
            assert success
            assert output_path.exists()
        
        manager.cleanup()


@pytest.fixture
def temp_config_file():
    """Fixture providing temporary config file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
camera:
  default_device_id: 0
  default_resolution: [1920, 1080]
capture:
  output_directory: captures
  image_format: jpg
""")
        config_path = f.name
    
    yield config_path
    
    # Cleanup
    Path(config_path).unlink(missing_ok=True)


class TestConfigManager:
    """Test configuration manager."""
    
    def test_default_config(self):
        """Test default configuration loading."""
        config = ConfigManager("non_existent_config.yaml")
        
        # Should have default values
        assert config.get("camera.default_device_id") == 0
        assert config.get("capture.image_format") == "jpg"
        assert config.get("ui.theme") == "light"
    
    def test_config_get_set(self):
        """Test getting and setting config values."""
        config = ConfigManager("test_config.yaml")
        
        # Test getting values
        assert config.get("camera.default_fps") == 30
        assert config.get("non.existent.key", "default") == "default"
        
        # Test setting values
        config.set("camera.default_fps", 60)
        assert config.get("camera.default_fps") == 60
        
        config.set("new.nested.key", "value")
        assert config.get("new.nested.key") == "value"
    
    def test_config_sections(self):
        """Test getting configuration sections."""
        config = ConfigManager("test_config.yaml")
        
        camera_config = config.get_camera_config()
        assert "default_device_id" in camera_config
        
        capture_config = config.get_capture_config()
        assert "output_directory" in capture_config
        
        ui_config = config.get_ui_config()
        assert "theme" in ui_config