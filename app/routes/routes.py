from .book import BookApi

def initialize_routes(api):
    api.add_resource(BookApi, '/book')