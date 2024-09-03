from os import getenv
from googleapiclient.errors import HttpError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_folder(service, folder_id):
    logger.info(f"Querying folder with ID: {folder_id}")

    # Get the folder's metadata to retrieve its name
    try:
        folder_metadata = (
            service.files()
            .get(
                fileId=folder_id,
                fields="name",
                supportsAllDrives=True,
            )
            .execute()
        )
        folder_name = folder_metadata["name"]

        logger.info(f"Folder name retrieved: {folder_name}")

        query = f"'{folder_id}' in parents"
        order_by = getenv("ORDER_BY")
        results = (
            service.files()
            .list(
                q=query,
                orderBy=order_by,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                fields="files(id, name, mimeType, parents)",
            )
            .execute()
        )

        logger.info(f"Results retrieved with {len(results.get('files', []))} items")

        # Add folder name to results
        results["folder_name"] = folder_name

        return results

    except HttpError as error:
        logger.error(f"HttpError: {error.resp.status} {error._get_reason()}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None


def query_file_metadata(service, file_id):
    try:
        file_metadata = (
            service.files()
            .get(fileId=file_id, fields="name, size, mimeType", supportsAllDrives=True)
            .execute()
        )
        return file_metadata

    except HttpError as error:
        logger.error(f"HttpError: {error.resp.status} {error._get_reason()}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
