import os
from sys import platform
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

    try:
        if platform in ["linux", "darwin"]:
            base_download_dir = os.environ["HOME"]
        elif platform in ["win32", "cygwin"]:
            base_download_dir = os.environ["USERPROFILE"]
        else:
            raise ValueError("Unsupported platform")

        # Define the destination folder
        base_download_dir = os.path.join(base_download_dir, "Downloads")

        # Create the "GDrive Downloads" folder inside the Downloads directory
        download_files.create_download_folder(base_download_dir, "GDrive Downloads")

        # Move into "GDrive Downloads" directory
        dest_folder = os.path.join(base_download_dir, "GDrive Downloads")

    except (KeyError, OSError) as e:
        print(f"Error: {e}")
        print("Please enter a path to save the files.")
        dest_folder = input("Destination: ")

        # # Custom path
        # dest_folder = 'C:\\Users\\user\\Downloads'

    # Load environment variables from .env file
    load_dotenv()

    # Query for the folder id
    folder_id = os.getenv("FOLDER_ID")

    if not folder_id:
        print("Please set the FOLDER_ID environment variable.")
        return

    # List all files
    try:
        download_files.download_all_files_in_folder(service, folder_id, dest_folder)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
