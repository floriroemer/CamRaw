#!/bin/bash
# Run script for Linux/macOS

echo "Starting CamRaw..."

# Check if dependencies are installed
if ! python3 -c "import cv2, PIL, numpy" &> /dev/null; then
    echo "Dependencies not found. Running installation..."
    ./install.sh
fi

# Run the application
python3 main.py