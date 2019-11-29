import os
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import urllib.request

MAIN_URL = 'https://pixabay.com/photos/search/'
DOWNLOAD_BASE_DIR = "/home/osboxes/Downloads/pixabay_photos/"
EMAIL_USERNAME = "test_mailing@mail.com"
EMAIL_PASSWORD = "testing123"

CATEGORIES = [{'Animals': 'https://pixabay.com/images/search/?cat=animals'}]

driver = None


def main():
    setup_display()

    #Scrape each category in the list of categories
    for category in CATEGORIES:
        for key, value in category.items():
            scrape_category(key, value)


def setup_display():
    display = Display(visible=1, size=(1024, 768))
    display.start()


def setup_selenium_driver(category_name):
    global driver

    chrome_options = Options()
    current_working_dir = DOWNLOAD_BASE_DIR + category_name + '/'
    prefs = {"download.default_directory": current_working_dir}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return current_working_dir


def scrape_category(category_name, category_url):
    global driver

    print(f'Scraping Category - {category_name}')
    current_working_dir = setup_selenium_driver(category_name)

    #if category directoy doesn't exist yet, create it
    if not os.path.isdir(current_working_dir):
        os.mkdir(current_working_dir)

    login()

    #Go to category page
    driver.get(category_url)

    num_of_pages = calc_num_of_pages()
    current_page_num = 1

    while category_has_next_page(current_page_num, num_of_pages):
        scrape_page(category_name, category_url, current_working_dir)
        next_page()
        current_page_num  += 1

#Download all images from a specific page
def scrape_page(category_name, page_url, current_working_dir):
    global driver

    #scroll to bottom of page
    driver.execute_script("window.scrollTo(0, 99999)")

    image_list = driver.find_elements_by_class_name('item')
    image_count = len(image_list)

    i = 0
    #Download image and return to category page when done
    #while i <= image_count:
    while i <= 4:
        image_list = driver.find_elements_by_class_name('item')
        image = image_list[i]
        print(f'Downloading image {i+1} of {image_count} in Category - {category_name}')
        image.click()
        image_id = generate_image_id(driver.current_url)
        download_image(current_working_dir,image_id)
        driver.get(page_url)
        i += 1


#Log into pixabay using provided email and password
def login():
    global driver, EMAIL_USERNAME, EMAIL_PASSWORD

    driver.get('https://pixabay.com/accounts/login/')
    time.sleep(10)
    driver.find_element_by_id('id_username').send_keys(EMAIL_USERNAME)
    driver.find_element_by_id('id_password').send_keys(EMAIL_PASSWORD)
    driver.find_element_by_class_name('sign_in_button').click()


#Download the image at the specified pixabay URL
def download_image(current_working_dir, image_id):
    global driver

    #create filename that image will be saved as
    save_dir = current_working_dir + image_id + '.png'

    #Do not download if image  has already been downloaded
    if check_if_already_downloaded(save_dir):
        print(f'Image {image_id} has already been downloaded.')
        return

    #Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, 99999)")

    #Click Free Download button
    free_download_button = driver.find_element_by_class_name('download_menu')
    free_download_button.click()

    #Click largest image size radio button
    radio_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div/table/tbody/tr[4]/td[1]/input')
    radio_button.click()

    #Download image directly
    image_link = driver.find_element_by_css_selector('a.dl_btn').get_attribute('href')
    image_link = image_link.replace('?attachment', '')
    #print(f' Download link is {image_link}')
    #print(driver.get_cookies()[0])
    driver.get(image_link)
    #urllib.request.urlretrieve(image_link, current_working_dir)
    #print(save_dir)
    #print(driver.get_cookies())
    driver.save_screenshot(save_dir)

#Generate unique image id from image url to be used as image file name
def generate_image_id(image_url):
    image_url = image_url.replace('https://pixabay.com/photos/', '')
    image_url = image_url.replace('/', '')
    return image_url

#check if the image has already been downloaded
def check_if_already_downloaded(save_dir):
    if os.path.isfile(save_dir):
        return True
    else:
        return False


def category_has_next_page(current_page_num, num_of_pages):
    if current_page_num <= num_of_pages:
        return True
    else:
        return False


#calculate the total number of pages in a given category
def calc_num_of_pages():
    global driver
    num_of_pages_element = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/h1')
    print(num_of_pages_element.get_attribute('outerHTML'))
    return 1


#advance the scraper to the next page of the category
def next_page():
    global driver
    pass


if __name__ == '__main__':
    main()
