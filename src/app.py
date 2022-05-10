from flask import Flask, render_template, jsonify, request, send_from_directory, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from scraper_book import ScraperBook
from picture import Picture
from dotenv import load_dotenv
from error.to_much_download_error import ToMuchDownloadError
from error.selenium_no_reachable import SeleniumNoReachable

load_dotenv('../.env')
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"": {"origins": "http://localhost:port"}})

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
                jsonify(
                    {   
                        "error": 'internal_server_error',
                        "message": 'Internal Server Error'
                    }
                ),
                500,
            )
            response.headers["Content-Type"] = "application/json"
            return response
    except ToMuchDownloadError as to_much_download:
        print(to_much_download.path)
        response = make_response(
                jsonify(
                    {   
                        "error": 'to_much_download',
                        "path": to_much_download.path
                    }
                ),
                200,
            )
        response.headers["Content-Type"] = "application/json"
        return response
    except FileNotFoundError:
        response = make_response(
                jsonify(
                    {   
                        "error": 'isbn_not_valid',
                        "message": 'the isbn filled is not valid'
                    }
                ),
                404,
            )
        response.headers["Content-Type"] = "application/json"
        return response
    except SeleniumNoReachable:
        response = make_response(
            jsonify(
                {   
                    "error": 'internal_server_error',
                    "message": 'Internal Server Error'
                }
            ),
            500,
        )
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == "__main__":
	app.run(port=3000, host='0.0.0.0')