import os
import os.path
import mimetypes
import json

from datetime import datetime
from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from Merge import Load,Save



def GenerateFileName():
    date_str = datetime.now().strftime('%Y-%m-%d')
    name = f'{date_str}_Alarmrapport.xlsx'
    return name

def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

def GetCreds():
    os.chdir(os.path.join(os.getcwd(),"data"))
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    token = "token.json"
    credentials ="credentials.json"
    
    
    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)

    if not creds or not creds.valid:
        if os.path.exists(token):
            os.remove(token)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token, 'x') as token:
            token.write(creds.to_json())
    os.chdir(os.path.dirname(os.getcwd()))
    return creds

def CheckFolder(FolderName, DriveID, service):
    # Check if the folder exists in the shared drive
    response = service.files().list(
        q=f"name='{FolderName}' and mimeType='application/vnd.google-apps.folder' and '{DriveID}' in parents and trashed=false",
        spaces='drive',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    folders = response.get('files', [])

    if not folders:
        # Query to find the folder in the Drive trash
        trash_response = service.files().list(
            q=f"name='{FolderName}' and mimeType='application/vnd.google-apps.folder' and trashed=true and '{DriveID}' in parents",
            spaces='drive',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        trash_folders = trash_response.get('files', [])

        if trash_folders:
            # Assuming there is exactly one folder matching the query
            folder_id = trash_folders[0]['id']

            # Restore the folder from trash
            restored_folder = service.files().update(
                fileId=folder_id,
                body={'trashed': False},
                supportsAllDrives=True
            ).execute()

            # Get the restored folder ID
            restored_folder_id = restored_folder['id']

            # Delete the restored folder
            service.files().delete(fileId=restored_folder_id, supportsAllDrives=True).execute()

            # Create a new folder in the shared drive
            file_metadata = {
                "name": FolderName,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [DriveID]
            }
            file = service.files().create(
                body=file_metadata,
                fields="id",
                supportsAllDrives=True
            ).execute()
            FolderID = file.get('id')
        else:
            # Folder does not exist, create it in the shared drive
            file_metadata = {
                "name": FolderName,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [DriveID]
            }
            file = service.files().create(
                body=file_metadata,
                fields="id",
                supportsAllDrives=True
            ).execute()
            FolderID = file.get('id')
    else:
        # Folder exists, get its ID
        FolderID = folders[0]['id']

    return FolderID


def UploadFile(File,FolderName,DriveID,key,**kwargs):
    creds = GetCreds()
    service = build('drive', 'v3', credentials=creds) 
    FolderID = CheckFolder(FolderName, DriveID, service)

    file_path = 'dates.json'
    file_path_data = Load(file_path)
    key_map = {'week': 'old_week', 'month': 'old_month'}
    key = key_map.get(key, key)
    if key in file_path_data.keys():
        file = file_path_data[key].split(".")[0] + ".xlsx"
        DeleteFile(file, FolderID, service)

    if key == 'last_day':
        current_date = datetime.now()
        six_months_prior = current_date - relativedelta(months=6)
        file_date = six_months_prior.strftime("%Y-%m")
        file = file_date + "_Alarmrapport.xlsx"
        DeleteFile(file, FolderID, service)
        

    if 'FileName' in kwargs:
        name = kwargs['FileName']
        FileName = name.split(".")[0] + ".xlsx"
    else:
        FileName = GenerateFileName()
        
        file_path = "dates.json"
        new_day = {
           "day": FileName
        }
        Save(new_day, file_path)

    try:
        file_metadata = {
        'name': FileName,
        'parents': [FolderID]
        }
        media = MediaFileUpload(File, resumable=True)
        # Create the file on the shared drive
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        ).execute()

        str = f'File with ID: "{file.get("id")}" has been uploaded.'
    except HttpError as error:
        str = f'An error occurred: {error}'
        file = None
    print(str)
    return str

def DeleteFile(FileName, DriveID, service):
    try:
        # Search for the file in the shared drive
        results = service.files().list(
            q=f"name='{FileName}' and '{DriveID}' in parents and trashed=false",
            corpora='allDrives ',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        items = results.get('files', [])
        if items:
            for item in items:
                file_id = item['id']
                service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
    except Exception as e:
        print(f"An error occurred: {e}")