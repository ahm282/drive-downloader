import os
from dotenv import load_dotenv
import authenticate_account
import download_files

def main():
    # Authenticate the account (login) and load the service
    service = authenticate_account.authenticate()

    # Set the destination folder to the Downloads folder
    # FIXME: On Windows and some Linux distributions, the Downloads folder is localised.
    # This works only on when the downloads folder is actually named "Downloads".
    # User can set the destination folder to a custom path.
    dest_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')

    # Custom path
    # dest_folder = 'C:\\Users\\user\\Downloads'

    # Load environment variables from .env file
    load_dotenv()

    # Query for the folder id
    folder_id = os.getenv('FOLDER_ID')

    if not folder_id:
        print('Please set the FOLDER_ID environment variable.')
        return

    query = f"'{folder_id}' in parents"

   # List the shared folders
    try:
        results = service.files().list(q=query, includeItemsFromAllDrives=True, supportsAllDrives=True, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found in the folder.')
        else:
            print(f"Found {len(items)} files in the folder.")
            for item in reversed(items):
                # FIXME: mkdir subfolders
                download_files.download_all_files_in_folder(service, item['id'], dest_folder)

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
