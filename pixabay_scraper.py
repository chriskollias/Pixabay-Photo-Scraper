from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

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
    display = Display(visible=0, size=(1024, 768))
    display.start()


def setup_selenium_driver(category_name):
    global driver

    chrome_options = Options()
    current_working_dir = DOWNLOAD_BASE_DIR + '/' + category_name + '/'
    prefs = {"download.default_directory": current_working_dir}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return current_working_dir


def scrape_category(category_name, category_url):
    global driver

    print(f'Scraping Category - {category_name}')
    current_working_dir = setup_selenium_driver(category_name)
    login()

    #Go to category page
    driver.get(category_url)

    #need to get list of pages here or do a while loop

    scrape_page(category_url, current_working_dir)


#Download all images from a specific page
def scrape_page(page_url, current_working_dir):
    global driver

    #scroll to bottom of page
    driver.execute_script("window.scrollTo(0, 99999)")

    image_list = driver.find_elements_by_class_name('item')
    image_count = len(image_list)

    i = 0
    #Download image and return to category page when done
    while i <= image_count:
        image_list = driver.find_elements_by_class_name('item')
        image = image_list[i]
        print(f'image count: {i}')
        print(f'current url {driver.current_url}')
        image.click()
        download_image(current_working_dir)
        print("Finished downloading, now returning to page")
        driver.get(page_url)
        i += 1

#Log into pixabay using provided email and password
def login():
    global driver, EMAIL_USERNAME, EMAIL_PASSWORD

    driver.get('https://pixabay.com/accounts/login/')
    driver.find_element_by_id('id_username').send_keys(EMAIL_USERNAME)
    driver.find_element_by_id('id_password').send_keys(EMAIL_PASSWORD)
    driver.find_element_by_class_name('sign_in_button').click()


#Download the image at the specified pixabay URL
def download_image(current_working_dir):
    global driver
    image_id = ''

    #Do not download if image  has already been downloaded
    if check_if_already_downloaded(current_working_dir, image_id):
        return

    #Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, 99999)")

    #Click Free Download button
    free_download_button = driver.find_element_by_class_name('download_menu')
    free_download_button.click()

    #Click largest image size radio button
    radio_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div/table/tbody/tr[4]/td[1]/input')
    radio_button.click()

    #Click image download button
    image_download_button = driver.find_element_by_class_name('dl_btn')
    image_download_button.click()



def check_if_already_downloaded(current_working_dir, image_id):
    return False


if __name__ == '__main__':
    main()
