from selenium import webdriver  # For dynamic web scraping
from selenium.webdriver.chrome.options import Options   # To add headless option (scrape without a chrome window)
import os, time, re
from urllib.request import urlretrieve # To save the scraped images
from picture import Picture
from os import listdir
from os.path import isfile, join
from error.to_much_download_error import ToMuchDownloadError


class ScraperImage:
    
    @staticmethod
    def imageScrape(term, var):
        """
            Récupérer les 1à premières images de la recherche google et les sauvegarder dans un bon directory

            Returns
                True si toutes les images sont bien scrap
                None si toutes les images sont pas bien scrap
        """

        # Replace each space with + character
        term = term.replace(' ', '+')

        # Create selenium web driver
        options = Options()
        #options.add_argument("--headless") # Run the webdriver without opening a browser window
        driver = webdriver.Chrome(options=options)
        isbn = 9782267027006

        url = f"https://fr.fr1lib.org/s/{isbn}?"
        driver.get(url)

        driver.implicitly_wait(1)

    

        #imgs = driver.find_element_by_id('searchResultBox') # Get first 10 images
        #print(imgs)

        book_research = driver.find_element_by_xpath("//h3[@itemprop='name']/a")
        href = book_research.get_attribute('href')
        book_id = href.split('/')[-2]
        print(book_id)
        urlBook = book_research.get_attribute('href')
        driver.get(urlBook)

        book_download = driver.find_element_by_xpath(f"//a[@data-isbn='{isbn}']")
        name_book = driver.find_element_by_xpath(f"//h1[@itemprop='name']").get_attribute("innerHTML").strip()
        url_download = book_download.get_attribute('href')
        print(name_book)
        print(url_download)
        try:
            driver.get(url_download)
            # download-limits-error__header
            content_page_to_much_download = driver.find_element_by_xpath(f"//h1[@class='download-limits-error__header']").get_attribute("innerHTML").strip()
            if content_page_to_much_download == "Vous avez atteint votre limite quotidienne":
                driver.quit()
                raise ToMuchDownloadError
        except:
            driver.quit()
            raise ToMuchDownloadError
    

        download_directroy = os.environ['DOWNLOAD_PATH']

        while(True):
            files = [f for f in listdir(download_directroy) if isfile(join(download_directroy, f))]
            print('-------------------------')
            count_max_seconds = 60
            for file in files:
                #print(file)
                #print(name_book.replace('\'', ''))
                if(re.match(r" *"  + name_book.replace('\'', '') + r" *" , file)):
                    return url_download + '/' + file
                    
            time.sleep(2)
            count_max_seconds -= 2
            if count_max_seconds == 0:
                break
        
        return False