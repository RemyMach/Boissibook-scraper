import requests
import os
from .extension_to_app_type import extension_to_app_type
from error.to_much_download_error import ToMuchDownloadError
from error.back_not_reachable import BackNotReachable
import logging
import logging.handlers

handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "scrapper.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
log.addHandler(handler)

def uploadFile(path, bookId):
    download_path = os.getenv('DOWNLOAD_PATH')
    base_path = os.getenv('BOISSIBOOK_API')

    url = f"{base_path}/book-files"

    for key in extension_to_app_type.keys():
        if(path.strip().endswith(key)):
            payload={'bookId': bookId, 'userId': None}
            files=[('file',(path, open(f"{download_path}/{path}" ,'rb'), extension_to_app_type[key]))]
            headers = {}
            try:
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
            except requests.exceptions.ConnectionError:
                log.info('erreur de connection vers le back')
                raise BackNotReachable
            if(response.status_code != 201):
                log.info("erreur de l'api bacl")
                log.info(response.status_code)
                log.info(response.text)
                raise BackNotReachable
            else:
                log.info(response.status_code)
                log.info(response.text)
            return

    log.info(f"error extension for {path}, not supported")   
