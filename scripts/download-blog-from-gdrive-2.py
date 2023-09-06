import io
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

FILE_KIND = "drive#file"
FOLDER_MIMETYPE = "application/vnd.google-apps.folder"
CRED_FILE = "/tmp/cred.json"

folder_id = os.environ.get("BLOG_FOLDER_ID")
cred_file_content = os.environ.get("BLOG_CRED_FILE_CONTENT")
with open(CRED_FILE, "w+") as fh:
    fh.write(cred_file_content)

creds = service_account.Credentials.from_service_account_file(
    CRED_FILE
)

service_v2 = build('drive', 'v2', credentials=creds)
service_v3 = build('drive', 'v3', credentials=creds)

def download_file(target_path, file_id: str):
    try:
        request = service_v3.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return

    with open(target_path, "wb+") as fh:
        print(f"writing to {target_path}...")
        fh.write(file.getvalue())

def download_folder(root: str, folder_id: str):
    if not os.path.exists(root):
        os.makedirs(root)
    f = service_v2.children().list(folderId=folder_id, maxResults=1000).execute()
    for child in f["items"]:
        child_details = service_v2.files().get(fileId=child["id"]).execute()
        if child_details["mimeType"] == FOLDER_MIMETYPE:
            download_folder(
                os.path.join(root, child_details["title"]),
                folder_id=child["id"]
            )
        else:
            target_path = os.path.join(root, child_details["title"])
            download_file(target_path, file_id=child["id"])


if __name__ == '__main__':
    download_folder(os.curdir, folder_id)