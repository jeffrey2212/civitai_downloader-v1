# Civitai Model Downloader

This Python script allows you to download AI models from the Civitai website by providing a markdown file with links to the models.

## Features

- Extracts model links from a markdown file
- Downloads models one by one
- Displays download progress like `wget`
- Handles errors and logs them
- Organizes downloaded models into folders based on their type
- Supports resuming downloads in case of interruption

## Requirements

- Python 3.6 or higher
- The following Python packages:
  - requests
  - tqdm

## Installation

1. Clone this repository or download the source files.
2. Install the required Python packages by running the following command in your terminal or command prompt:

   ```
   python -m pip install -r requirements.txt
   ```

## Usage

```
python main.py -file <input_markdown_file> [-path <optional_download_folder>]
```

- `<input_markdown_file>`: The path to the markdown file containing model links
- `<optional_download_folder>` (optional): The path to the folder where the downloaded models will be stored. If not provided, models will be stored in the current working directory.

## Example

```bash
python main.py -file file.md -path filepath
```
