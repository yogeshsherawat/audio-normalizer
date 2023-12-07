# Normalizer

## Overview

Welcome to Normalizer, a Python application designed to normalize the loudness of audio files. This simple tool ensures consistent audio volume levels, enhancing the listening experience.

## Features

- **Loudness Normalization:** Bring uniformity to the loudness of your audio files.
- **Easy-to-Use:** Simple command-line interface for quick and hassle-free loudness normalization.
- **Supported Formats:** Works with popular audio formats such as WAV, MP3, and more.

## Getting Started

### Prerequisites

- Python 3.7>= installed on your system.

### Installation


   ```bash
   git clone https://github.com/yourusername/normalizer.git
   cd normalizer
   pip install -r requirements.txt
   python main.py 
   ```

### Preparing standalone app for mac 
- Use Below Two Commands
- > pyinstaller --onefile --windowed --clean --noupx main.py     
- > create-dmg 'dist/main.app' --overwrite --dmg-title=Normalizer

### Preparing Standalone App For Windows


