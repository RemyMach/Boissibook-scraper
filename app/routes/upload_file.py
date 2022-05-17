import requests
import os
from dotenv import load_dotenv
from .extension_to_app_type import extension_to_app_type

load_dotenv()

def uploadFile(path, bookId):
    download_path = os.getenv('DOWNLOAD_PATH')
    base_path = os.getenv('BOISSIBOOK_API')

    url = f"{base_path}/book-files"

    for key in extension_to_app_type.keys():
        if(path.endswith(key)):
            payload={'bookId': bookId}
            files=[('file',(path, open(f"{download_path}/{path}" ,'rb'), extension_to_app_type[key]))]
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            return
            
    print(f"error extension for {path}, not supported")