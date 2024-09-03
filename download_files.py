import io
import os

from tqdm import tqdm
from googleapiclient.http import MediaIoBaseDownload


def create_download_folder(destination_folder, new_subfolder):
    script_downloads_folder = destination_folder + f"\\{new_subfolder}"
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

    file_metadata = (
        service.files()
        .get(fileId=file_id, fields="name, size", supportsAllDrives=True)
        .execute()
    )
    file_size = int(file_metadata.get("size"))
    file_name = file_metadata.get("name")

    req = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, mode="wb")
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


# FIXME: Implement function to query google drive api to handle subfolders.
def download_all_files_in_folder(service, folder_id, destination_folder):
    target_subfolder = "GDrive Downloads"
    query = f"'{folder_id}' in parents"
    results = (
        service.files()
        .list(
            q=query,
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            fields="files(id, name, mimeType)",
        )
        .execute()
    )

    items = results.get("files", [])

    if not items:
        return "No files found in the folder to be downloaded."

    if create_download_folder(destination_folder, target_subfolder) == 0:
        destination_folder = destination_folder + f"\\{target_subfolder}"

    for item in reversed(items):
        try:
            destination_path = os.path.join(destination_folder, item["name"])
            download_file(service, item["id"], destination_path)
        except Exception as e:
            print(
                f"/{item['name']}: Unable to download subfolders at the moment. Skipping...\n"
            )
