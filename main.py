#!/usr/bin/env python3
"""
CamRaw - Simple Python Camera Application
Main entry point for the application.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from camraw import CameraApp


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="CamRaw - Simple Python Camera Application"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/settings.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="captures",
        help="Directory to save captured images"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run in headless mode (CLI only)"
    )
    
    args = parser.parse_args()
    
    try:
        app = CameraApp(
            config_path=args.config,
            output_dir=args.output_dir,
            debug=args.debug,
            headless=args.no_gui
        )
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting CamRaw: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()