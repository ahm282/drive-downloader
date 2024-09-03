def query_folder(service, folder_id):
    # FIXME: Implement error handling
    # Get the folder's metadata to retrieve its name
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

    query = f"'{folder_id}' in parents"
    results = (
        service.files()
        .list(
            q=query,
            orderBy="name",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            fields="files(id, name, mimeType, parents)",
        )
        .execute()
    )

    # Add folder name to results
    results["folder_name"] = folder_name

    return results


def query_file_metadata(service, file_id):
    # FIXME: Implement error handling
    file_metadata = (
        service.files()
        .get(fileId=file_id, fields="name, size, mimeType", supportsAllDrives=True)
        .execute()
    )

    return file_metadata
