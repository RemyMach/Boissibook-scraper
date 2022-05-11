from selenium import webdriver  # For dynamic web scraping
from selenium.webdriver.chrome.options import Options   # To add headless option (scrape without a chrome window)
import os, time, re
from urllib.request import urlretrieve # To save the scraped images
from os import listdir
from os.path import isfile, join
from error.to_much_download_error import ToMuchDownloadError
from error.selenium_no_reachable import SeleniumNoReachable
from selenium.common.exceptions import NoSuchElementException


class ScraperBook:
    
    @staticmethod
    def bookScrape(isbn):
        
        SECONDS_LIMIT_DOWNLOAD = 20
        # Create selenium web driver
        options = Options()
        options.add_argument("--headless") # Run the webdriver without opening a browser window
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        # Go to the home page
        try:
            url = f"https://fr.fr1lib.org/s/{isbn}?"

            driver.get(url)
            driver.implicitly_wait(1)
        except:
            driver.quit()
            raise SeleniumNoReachable

        # get the first link book in the list
        try:
            book_research = driver.find_element_by_xpath("//h3[@itemprop='name']/a")
            urlBook = book_research.get_attribute('href')
        except NoSuchElementException:
            driver.quit()
            raise FileNotFoundError
        
        book_id = urlBook.split('/')[-2]

        # get the element by isbn and the download url
        try:
            driver.get(urlBook)
            book_download = driver.find_element_by_xpath(f"//a[@data-isbn='{isbn}']")
            name_book = driver.find_element_by_xpath(f"//h1[@itemprop='name']").get_attribute("innerHTML").strip()
            url_download = book_download.get_attribute('href')
        except NoSuchElementException:
            driver.quit()
            raise FileNotFoundError

        try:
            driver.get(url_download)
            content_page_to_much_download = driver.find_element_by_xpath(f"//h1[@class='download-limits-error__header']").get_attribute("innerHTML").strip()
            if content_page_to_much_download == "Vous avez atteint votre limite quotidienne":
                driver.quit()
                raise ToMuchDownloadError(url_download)
        except ToMuchDownloadError:
            driver.quit()
            raise ToMuchDownloadError(url_download)
        except NoSuchElementException:
            pass

        driver.quit()

        # search if the folder is in the download directory
        download_directroy = os.environ['DOWNLOAD_PATH']
        count_max_seconds = SECONDS_LIMIT_DOWNLOAD
        while(count_max_seconds != 0):

            files = [f for f in listdir(download_directroy) if isfile(join(download_directroy, f))]
            for file in files:
                if(re.match(r" *"  + name_book.replace('\'', '') + r" *" , file)):
                    return file

            count_max_seconds -= 2
            time.sleep(2)
        
        raise ToMuchDownloadError(url_download)