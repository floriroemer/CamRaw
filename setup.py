"""
Setup script for CamRaw package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip()
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="camraw",
    version="0.1.0",
    author="Florian Roemer",
    author_email="support@camraw.example.com",
    description="A simple and intuitive Python camera application for desktop computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/floriroemer/CamRaw",
    project_urls={
        "Bug Reports": "https://github.com/floriroemer/CamRaw/issues",
        "Source": "https://github.com/floriroemer/CamRaw",
        "Documentation": "https://camraw.readthedocs.io",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "gui": [
            "PyQt6>=6.5.0",
        ],
        "raw": [
            "rawpy>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "camraw=camraw:main",
        ],
    },
    include_package_data=True,
    package_data={
        "camraw": ["config/*.yaml"],
    },
    keywords="camera photography image capture raw processing desktop",
    zip_safe=False,
)