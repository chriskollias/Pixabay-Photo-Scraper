from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


DOWNLOAD_BASE_DIR = "/home/osboxes/Downloads/pixabay_photos/"
email_username = "test_mailing@mail.com"
email_password = "testing123"

display = Display(visible=0, size=(1024, 768))
display.start()

chrome_options = Options()
prefs = {"download.default_directory": DOWNLOAD_BASE_DIR}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)


#Login
driver.get('https://pixabay.com/accounts/login/')

driver.find_element_by_id('id_username').send_keys(email_username)
driver.find_element_by_id('id_password').send_keys(email_password)

driver.find_element_by_class_name('sign_in_button').click()

driver.get('https://pixabay.com/images/search/')
print(driver.title)

#driver.find_element_by_id('q').send_keys('test')

print(driver.current_url)

driver.execute_script("window.scrollTo(0, 99999)")

#image_grid = driver.find_element_by_class_name('flex_grid')
image_list = driver.find_elements_by_class_name('item')

i = 1
for image in image_list:
    print(f'image count: {i}')
    image.click()

    driver.execute_script("window.scrollTo(0, 99999)")

    #Click Free Download button
    free_download_button = driver.find_element_by_class_name('download_menu')
    print(f"WHAT THE HELL IS THIS? {free_download_button.get_attribute('outerHTML')}")
    free_download_button.click()


    #Click largest image size radio button
    radio_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div/table/tbody/tr[4]/td[1]/input')
    radio_button.click()
    #print("test!", radio_button)

    #Click image download button
    image_download_button = driver.find_element_by_class_name('dl_btn')
    image_download_button.click()

    print(driver.current_url)

    i += 1