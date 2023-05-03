import requests
import json
import re
import os
import argparse
import sys
from PIL import Image
from tqdm import tqdm


def get_download_link(url):
    model_id = url.split('/')[-2]
    if model_id.isdigit() != True:
        model_id = url.split('/')[-1]

    api_url = f"https://civitai.com/api/v1/models/{model_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        model_file = None
        for file in data.get("modelVersions")[0]["files"]:
            if file["type"] in ("Model", "Negative"):
                model_file = file
                break

        if model_file:
            download_link = model_file["downloadUrl"]
            filename = model_file['name']
            model_type = data['type']
            return download_link, filename, model_type, data
    return None, None, None, None


def extract_links_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    link_pattern = r'(?:(?:\[[^\]]*]\()|(?:^|[^\(]))(https?://\S+?)(?:\)|\s|$)'
    links = re.findall(link_pattern, content)

    return links


def download_file(url, file_path):
    # Check if the file already exists
    if os.path.exists(file_path):
        print(
            f"File '{os.path.basename(file_path)}' already exists. Skipping download.")
        return True

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for data in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB', ncols=100):
                file.write(data)
    else:
        return False
    return True


def download_preview(data, filename, destination_folder):
    images = data.get("modelVersions")[0].get("images")
    if images:
        preview_url = images[0].get("url")
        preview_ext = os.path.splitext(preview_url)[1]
        filename_without_ext = os.path.splitext(filename)[0]
        preview_path = os.path.join(
            destination_folder, f"{filename_without_ext}.png")

        if not os.path.exists(preview_path):
            response = requests.get(preview_url, stream=True)
            if response.status_code == 200:
                with open(preview_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                if preview_ext.lower() != '.png':
                    img = Image.open(preview_path)
                    img.save(preview_path, 'PNG')
            else:
                print(f"Failed to download preview image: {preview_url}")
        else:
            print(
                f"Preview image '{filename_without_ext}.png' already exists. Skipping download.")


def main():
    parser = argparse.ArgumentParser(
        description='Download models from Civitai')
    parser.add_argument('-file', type=str, required=True,
                        help='Markdown file containing model links')
    parser.add_argument('-path', type=str, default='',
                        help='Optional destination folder')

    args = parser.parse_args()

    file_path = args.file
    base_destination_folder = args.path

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    links = extract_links_from_markdown(file_path)

    for link in links:
        download_link, filename, model_type, data = get_download_link(link)

        if download_link and filename and model_type:
            destination_folder = base_destination_folder
            if destination_folder:
                destination_folder = os.path.join(
                    destination_folder, model_type)
            else:
                destination_folder = model_type

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            output_path = os.path.join(destination_folder, filename)
            print(f"Downloading {filename}...")

            if download_file(download_link, output_path):
                print(f"{filename} downloaded successfully.")
                download_preview(data, filename, destination_folder)
            else:
                print(f"Error: Failed to download {filename}.")
        else:
            print(f"Error: Unable to get download link for {link}.")


if __name__ == '__main__':
    main()
