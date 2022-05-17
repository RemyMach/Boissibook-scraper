from flask import Response, request
from flask_restful import Resource
from flask import Flask, render_template, jsonify, request, send_from_directory, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from .scraper_book import ScraperBook
from dotenv import load_dotenv
from error.to_much_download_error import ToMuchDownloadError
from error.selenium_no_reachable import SeleniumNoReachable
import os
from response.error_response import ErrorResponse
from response.to_much_download_response import ToMuchDownloadResponse
from .upload_file import uploadFile


class BookApi(Resource):
    def post(self):

        isbn = request.get_json()['isbn']
        bookId = request.get_json()['bookId']

        print(isbn)

        try: 
            file = ScraperBook.bookScrape(isbn, bookId)
            try:
                download_directory = os.environ['DOWNLOAD_PATH']
                uploadFile(file, bookId)
                response = make_response(
                    {'status': "DOWNLOAD_SUCCESS"},
                    200,
                )
                response.headers["Content-Type"] = "application/json"
                return response
            except FileNotFoundError:
                response = make_response(
                    ErrorResponse('internal_server_error',  'Internal Server Error').__dict__,
                    500,
                )
                response.headers["Content-Type"] = "application/json"
                return response
        except ToMuchDownloadError as to_much_download:
            print(to_much_download.path)
            response = make_response(
                    ToMuchDownloadResponse('to_much_download',  to_much_download.path).__dict__,
                    200,
                )
            response.headers["Content-Type"] = "application/json"
            return response
