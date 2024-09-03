import io
import os
from time import sleep
from query_gdrive import query_folder, query_file_metadata

from tqdm import tqdm
from googleapiclient.http import MediaIoBaseDownload


def create_download_folder(destination_folder, new_subfolder_name):
    script_downloads_folder = destination_folder + f"\\{new_subfolder_name}"
    exit_value = 0

    try:
        if not os.path.exists(script_downloads_folder):
            os.mkdir(script_downloads_folder)
    except OSError as e:
        exit_value = 1
        print(e)

    return exit_value


def download_file(service, file_id, destination):
    if os.path.exists(destination):
        return f"File {destination} already exists. Skipping..."

    metadata = query_file_metadata(service, file_id)

    file_size = int(metadata.get("size"))
    file_name = metadata.get("name")

    try:
        req = service.files().get_media(fileId=file_id)

        with io.FileIO(destination, mode="wb") as fh:
            print(f"Starting download: {destination}")
            downloader = MediaIoBaseDownload(fh, req)

            done = False

            with tqdm(
                total=file_size, unit="MB", unit_scale=True, desc=file_name, initial=0
            ) as pbar:
                while not done:
                    status, done = downloader.next_chunk()

                    if status:
                        pbar.update(status.resumable_progress - pbar.n)

            print(f"Downloaded {destination}", end="\n\n")
    # FIXME: Better implementation needed to gracefully abort script
    except KeyboardInterrupt:
        print("Aborting download...")


def download_subfolder_content(service, folder_id, destination_folder):
    subfolder = query_folder(service, folder_id)

    subfolder_name = subfolder["folder_name"]
    subfolder_content = subfolder.get("files")

    # Create a subfolder
    if create_download_folder(destination_folder, subfolder_name) == 0:
        destination_folder = destination_folder + f"\\{subfolder_name}"

    # Download content
    for item in subfolder_content:
        destination_path = os.path.join(destination_folder, item["name"])
        download_file(service, item["id"], destination_path)


def download_all_files_in_folder(service, folder_id, destination_folder):
    query_results = query_folder(service, folder_id)
    items = query_results.get("files", [])

    if not items:
        return "No files found in the folder to be downloaded."

    if create_download_folder(destination_folder, query_results["folder_name"]) == 0:
        destination_folder = os.path.join(
            destination_folder, query_results["folder_name"]
        )

    for item in items:
        try:
            if item["mimeType"] != "application/vnd.google-apps.folder":
                destination_path = os.path.join(destination_folder, item["name"])
                download_file(service, item["id"], destination_path)
            else:  # Item is a subfolder
                download_subfolder_content(service, item["id"], destination_folder)

            # FIXME: Sleep for 1 sec to be able to exit script without moving first to the next file
            sleep(1)
        except Exception as e:
            print(e)
