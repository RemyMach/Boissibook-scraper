from selenium import webdriver  # For dynamic web scraping
from selenium.webdriver.chrome.options import Options   # To add headless option (scrape without a chrome window)
import os, time, re
from urllib.request import urlretrieve # To save the scraped images
from picture import Picture
from os import listdir
from os.path import isfile, join
from error.to_much_download_error import ToMuchDownloadError
from selenium.common.exceptions import NoSuchElementException


class ScraperImage:
    
    @staticmethod
    def imageScrape(isbn):
        """
            Récupérer les 1à premières images de la recherche google et les sauvegarder dans un bon directory

            Returns
                True si toutes les images sont bien scrap
                None si toutes les images sont pas bien scrap
        """
        
        SECONDS_LIMIT_DOWNLOAD = 20
        # Create selenium web driver
        options = Options()
        #options.add_argument("--headless") # Run the webdriver without opening a browser window
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        try:
            url = f"https://fr.fr1lib.org/s/{isbn}?"
            driver.get(url)
            driver.implicitly_wait(1)
        except:
            driver.quit()
            raise FileNotFoundError

        try:
            book_research = driver.find_element_by_xpath("//h3[@itemprop='name']/a")
            href = book_research.get_attribute('href')
        except NoSuchElementException:
            driver.quit()
            raise FileNotFoundError
        
        book_id = href.split('/')[-2]
        urlBook = book_research.get_attribute('href')
        try:
            driver.get(urlBook)
            print('après url book')
            book_download = driver.find_element_by_xpath(f"//a[@data-isbn='{isbn}']")
            name_book = driver.find_element_by_xpath(f"//h1[@itemprop='name']").get_attribute("innerHTML").strip()
            url_download = book_download.get_attribute('href')
        except NoSuchElementException:
            driver.quit()
            raise FileNotFoundError
        
        print(name_book)
        print(url_download)
        try:
            print("je suis une pomme 1")
            driver.get(url_download)
            print("je suis une pomme 2")
            content_page_to_much_download = driver.find_element_by_xpath(f"//h1[@class='download-limits-error__header']").get_attribute("innerHTML").strip()
            if content_page_to_much_download == "Vous avez atteint votre limite quotidienne":
                print(content_page_to_much_download)
                driver.quit()
                raise ToMuchDownloadError(url_download)
        except ToMuchDownloadError:
            driver.quit()
            raise ToMuchDownloadError(url_download)
        except NoSuchElementException:
            print('on a pas dépassé la limite de download')


        print('on arrive ici')

        download_directroy = os.environ['DOWNLOAD_PATH']

        while(True):
            files = [f for f in listdir(download_directroy) if isfile(join(download_directroy, f))]
            print('-------------------------')
            count_max_seconds = SECONDS_LIMIT_DOWNLOAD
            for file in files:
                if(re.match(r" *"  + name_book.replace('\'', '') + r" *" , file)):
                    return file
                    
            time.sleep(2)
            count_max_seconds -= 2
            if count_max_seconds == 0:
                raise ToMuchDownloadError(url_download)
        
        driver.quit()
        
        return False