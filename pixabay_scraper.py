from selenium import webdriver

browser = None
MAIN_URL = 'https://pixabay.com/photos/search/'

def main():
    setup()


def setup():
    global browser
    #browser = webdriver.Firefox()
    #browser.implicitly_wait(10)
    #browser.get(MAIN_URL)

def scrape_category():
    pass

def download_picture():
    pass

def check_if_already_downloaded(picture_id):
    pass

if __name__ == '__main__':
    main()

