from flask import Flask, render_template, jsonify, request, send_from_directory, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from scraper_book import ScraperBook
from dotenv import load_dotenv
from error.to_much_download_error import ToMuchDownloadError
from error.selenium_no_reachable import SeleniumNoReachable
import os
from response.error_response import ErrorResponse
from response.to_much_download_response import ToMuchDownloadResponse

load_dotenv('../.env')
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"": {"origins": "*"}})

@app.route('/book/<isbn>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getFile(isbn):

    try: 
        file = ScraperBook.bookScrape(isbn)
        try:
            download_directory = os.environ['DOWNLOAD_PATH']
            return send_from_directory(download_directory, file, as_attachment=True)
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
    except FileNotFoundError:
        response = make_response(
                ErrorResponse('isbn_not_valid',  'the isbn filled is not valid').__dict__,
                404,
            )
        response.headers["Content-Type"] = "application/json"
        return response
    except SeleniumNoReachable:
        response = make_response(
                ErrorResponse('internal_server_error',  'Internal Server Error').__dict__,
                500,
            )
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == "__main__":
	app.run(port=3000, host='0.0.0.0')