class ToMuchDownloadError(Exception):
    def __init__(self, path):
        self.path = path
    pass
