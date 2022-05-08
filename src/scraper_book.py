from selenium import webdriver  # For dynamic web scraping
from selenium.webdriver.chrome.options import Options   # To add headless option (scrape without a chrome window)
import os, time
from urllib.request import urlretrieve # To save the scraped images
from picture import Picture

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
        url_download = book_download.get_attribute('href')
        print(url_download)
        driver.get(url_download)

        #If image is fetched correctly, download it and save it in a file
        try:
            #urlretrieve(url_download, f"static/{isbn}")
            #encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request(url_download)
            redirected_url = urllib.request.urlopen(req).geturl()
            print(redirected_url)
            #urlretrieve('https://swab.zlibcdn.com/dtoken/a7328189a1c7374fd64d1d1044fe1832', f"static/{isbn}.epub")
        except:
            # An error in the link happened
            print('[WARNING] Image number %d failed when downloading images for search term: %s' % (count, term))

        for(i in range(0, 60)):
            
            time(2)
        
        return True