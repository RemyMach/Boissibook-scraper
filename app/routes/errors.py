class FileNotFoundError(Exception):
    pass

errors = {
    "FileNotFoundError": {
        "error": 'isbn_not_valid',
        "message": 'the isbn filled is not valid',
        "status": 404
    },
    "SeleniumNoReachable": {
        "error": 'internal_server_error',
        "message": 'internal server error',
        "status": 500
    },
    "InternalServerError": {
        "error": 'internal_server_error',
        "message": 'internal server error',
        "status": 500
    }
}