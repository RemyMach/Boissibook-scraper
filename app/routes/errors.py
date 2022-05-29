class FileNotFoundError(Exception):
    pass

errors = {
    "FileNotFoundError": {
        "error": 'isbn_not_valid',
        "message": 'the isbn filled is not valid or we don\'t find it',
        "status": 404
    },
    "SeleniumNoReachable": {
        "error": 'internal_server_error',
        "message": 'please retry later our services are not available',
        "status": 500
    },
    "InternalServerError": {
        "error": 'internal_server_error',
        "message": 'please retry later our services are not available',
        "status": 500
    },
    "BackNotReachable": {
        "error": 'internal_server_error',
        "message": 'please retry later our services are not available',
        "status": 500
    },
    "InternalError": {
        "error": 'internal_server_error',
        "message": 'please retry later our services are not available',
        "status": 500
    },
}