import io
import os
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

FILE_KIND = "drive#file"
FOLDER_MIMETYPE = "application/vnd.google-apps.folder"
CRED_FILE = "/tmp/cred.json"
SKIP_FOLDERS = {"_drafts"}
MAX_RETRIES = 5

folder_id = os.environ.get("BLOG_FOLDER_ID")
cred_file_content = os.environ.get("BLOG_CRED_FILE_CONTENT")
with open(CRED_FILE, "w+") as fh:
    fh.write(cred_file_content)

creds = service_account.Credentials.from_service_account_file(
    CRED_FILE
)

service_v2 = build('drive', 'v2', credentials=creds)
service_v3 = build('drive', 'v3', credentials=creds)


def execute_with_retry(fn):
    """Execute a Drive API call with exponential backoff on transient errors."""
    for attempt in range(MAX_RETRIES):
        try:
            return fn()
        except HttpError as error:
            status = getattr(error.resp, "status", None)
            if status in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                delay = 2 ** attempt
                print(f"Transient HTTP {status}, retrying in {delay}s...")
                time.sleep(delay)
                continue
            raise


def download_file(target_path, file_id: str):
    def _download():
        request = service_v3.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()
        return file

    file = execute_with_retry(_download)
    with open(target_path, "wb+") as fh:
        print(f"writing to {target_path}...")
        fh.write(file.getvalue())


def download_folder(root: str, folder_id: str):
    if not os.path.exists(root):
        os.makedirs(root)
    f = execute_with_retry(
        lambda: service_v2.children().list(folderId=folder_id, maxResults=1000).execute()
    )
    for child in f["items"]:
        child_details = execute_with_retry(
            lambda cid=child["id"]: service_v2.files().get(fileId=cid).execute()
        )
        title = child_details["title"]
        if child_details["mimeType"] == FOLDER_MIMETYPE:
            if title in SKIP_FOLDERS:
                print(f"skipping folder {os.path.join(root, title)}...")
                continue
            download_folder(
                os.path.join(root, title),
                folder_id=child["id"]
            )
        else:
            target_path = os.path.join(root, title)
            download_file(target_path, file_id=child["id"])


if __name__ == '__main__':
    download_folder(os.curdir, folder_id)