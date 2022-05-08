from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from scraper_book import ScraperImage
from picture import Picture
from dotenv import load_dotenv
from error.to_much_download_error import ToMuchDownloadError

load_dotenv('../.env')
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"": {"origins": "http://localhost:port"}})

@app.route('/pictures', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def createPicture():

    # récupérer toute la post request en dict
    picture = request.get_json()
    # convertir le dictionnaire en objet Message
    picture = Picture(picture['name'])
    try: 
        file = ScraperImage.imageScrape(picture.name, picture.name)
    except ToMuchDownloadError:
        return "can't download"

    return file


if __name__ == "__main__":
	app.run(port=3000)