#!/usr/bin/env python3
"""
Utility functions for ETBD project
"""

import os
import datetime
from pathlib import Path

def ensure_directories():
    """Ensure that data and figures directories exist"""
    # Get the project root (parent of scripts_notebooks)
    project_root = Path(__file__).parent.parent
    
    # Create directories if they don't exist
    data_dir = project_root / "data"
    figures_dir = project_root / "figures"
    
    data_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(exist_ok=True)
    
    return data_dir, figures_dir

def get_timestamped_filename(base_name, extension):
    """Generate a timestamped filename"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"

def save_plot(fig, filename, dpi=300, bbox_inches='tight'):
    """Save a plot to the figures directory"""
    data_dir, figures_dir = ensure_directories()
    
    # Add timestamp if filename doesn't already have one
    if '_' not in filename or not any(char.isdigit() for char in filename):
        name, ext = os.path.splitext(filename)
        filename = get_timestamped_filename(name, ext[1:])
    
    filepath = figures_dir / filename
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"✓ Plot saved as '{filepath}'")
    return filepath

def save_data(data, filename):
    """Save data to the data directory"""
    data_dir, figures_dir = ensure_directories()
    
    # Add timestamp if filename doesn't already have one
    if '_' not in filename or not any(char.isdigit() for char in filename):
        name, ext = os.path.splitext(filename)
        filename = get_timestamped_filename(name, ext[1:])
    
    filepath = data_dir / filename
    data.to_csv(filepath, index=False)
    print(f"Data saved as '{filepath}'")
    return filepath

def get_output_paths():
    """Get the paths for data and figures directories"""
    data_dir, figures_dir = ensure_directories()
    return data_dir, figures_dir
