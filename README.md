# GDrive Downloader

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Drive API](https://img.shields.io/badge/Google%20Drive%20API-4285F)
![GitHub license](https://img.shields.io/github/license/ahm282/gdrive-downloader)

**Status: Work in Progress (WIP)**

## Overview

This project is a file downloader for Google Drive. The goal of this project is to automate (bulk) downloads from Google Drive and easily download files from Google Drive without a GUI.
Google automatically zips files when downloading multiple files, which can be a hassle to wait for the files to get zipped, the download itself and unzipping the files afterwards.
This project downloads files without zipping them.
The project is built using Python and the Google Drive API.

## Getting Started

### Prerequisites

Ensure you have the following installed:
 
- Python 3.6 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ahm282/gdrive-downloader.git
    ```
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
3. Create a Google Cloud Platform project and enable the Google Drive API. Follow the instructions [here](https://developers.google.com/drive/api/v3/quickstart/python) to enable the API and download the `credentials.json` file.

4. Move the `credentials.json` file to the root of the project.

5. Add the folder ID of the Google Drive folder you want to download from in the `.env` file:

   ```python
   FOLDER_ID= "<folder_id>"
   ```  
6. Add the path to the folder where you want to download the files to in the `main.py` file:

   ```python
   dest_folder= "download path"
   ```
the script will look for the Downloads folder in your home directory by default.
but because the script is not yet able to handle localizations, sometimes you'll have to provide a different path.

6. Run the script:

   ```bash
   python main.py
   ```