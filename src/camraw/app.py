"""
Main application class for CamRaw.
"""

import logging
from pathlib import Path
from typing import Optional

from .camera import CameraManager
from .ui import MainWindow
from .config import ConfigManager
from .utils import setup_logging, ensure_directory


class CameraApp:
    """Main application class that coordinates all components."""
    
    def __init__(
        self,
        config_path: str = "config/settings.yaml",
        output_dir: str = "captures",
        debug: bool = False,
        headless: bool = False
    ):
        """
        Initialize the CamRaw application.
        
        Args:
            config_path: Path to configuration file
            output_dir: Directory to save captured images
            debug: Enable debug logging
            headless: Run without GUI
        """
        self.debug = debug
        self.headless = headless
        self.output_dir = Path(output_dir)
        
        # Setup logging
        setup_logging(debug=debug)
        self.logger = logging.getLogger(__name__)
        
        # Ensure output directory exists
        ensure_directory(self.output_dir)
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.camera_manager = CameraManager(self.config_manager)
        
        if not headless:
            self.ui = MainWindow(self.camera_manager, self.output_dir)
        else:
            self.ui = None
            
        self.logger.info("CamRaw application initialized")
    
    def run(self):
        """Start the application."""
        self.logger.info("Starting CamRaw application")
        
        try:
            # Initialize camera
            if not self.camera_manager.initialize():
                self.logger.error("Failed to initialize camera")
                return False
            
            if self.headless:
                self._run_headless()
            else:
                self._run_gui()
                
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            return False
        finally:
            self.cleanup()
        
        return True
    
    def _run_gui(self):
        """Run the GUI version of the application."""
        if self.ui:
            self.ui.show()
    
    def _run_headless(self):
        """Run the headless version of the application."""
        self.logger.info("Running in headless mode")
        # Basic CLI functionality can be implemented here
        print("CamRaw running in headless mode. Press Ctrl+C to exit.")
        
        # Keep the application running
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    def cleanup(self):
        """Clean up resources."""
        self.logger.info("Cleaning up application resources")
        
        if self.camera_manager:
            self.camera_manager.cleanup()
        
        if self.ui:
            self.ui.close()