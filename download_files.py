import io
import os

from tqdm import tqdm
from googleapiclient.http import MediaIoBaseDownload

def download_file(service, file_id, destination):
    if os.path.exists(destination):
        print(f"File {destination} already exists. Skipping...")
        return

    file_metadata = service.files().get(fileId=file_id, fields='size', supportsAllDrives=True).execute()
    file_size = int(file_metadata.get('size'))

    req = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, mode='wb')
    downloader = MediaIoBaseDownload(fh, req)
    done = False

    with tqdm(total=file_size, unit='MB', unit_scale=True, desc=destination, initial=0, ascii=True) as pbar:
        while not done:
            status, done = downloader.next_chunk()

            if status:
                pbar.update(status.resumable_progress - pbar.n)

    print(f"Downloaded {destination}")


def download_all_files_in_folder(service, folder_id, destination_folder):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, includeItemsFromAllDrives=True, supportsAllDrives=True, fields="files(id, name)").execute()

    items = results.get('files', [])

    if not items:
        print('No files found in the folder to be downloaded.')
    else:
        for item in reversed(items):
            print(f"Found {item['name']} - ({item['id']})")

            destination_path = os.path.join(destination_folder, item['name'])
            download_file(service, item['id'], destination_path)
