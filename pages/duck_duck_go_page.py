from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class SearchResultsPage:
    # locators
    images_grid = (By.CLASS_NAME, "js-images-thumbnails")
    list_elements = (
        By.CSS_SELECTOR,
        ".react-results--main li[data-layout='organic'] article:nth-child(1) h2 a span",
    )

    #
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def perform_search(self, text):
        search_bar = self.driver.find_element(By.ID, "searchbox_input")
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, ".searchbox_searchButton__F5Bwq"
        )
        search_bar.send_keys(text)
        search_button.click()

    def confirm_images_present(self):
        try:
            WebDriverWait(self.driver, 7).until(
                lambda driver: len(driver.find_elements(*self.images_grid)) > 0
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "Search for this parameter did not have images available"
            )

    def get_image_urls(self):
        images_grid = self.driver.find_element(*self.images_grid)
        image_divs = images_grid.find_elements(By.CSS_SELECTOR, ".js-images-link")
        image_urls_array = []

        for image_div in image_divs:
            anchor_in_div = image_div.find_element(By.TAG_NAME, "a")
            image_url = anchor_in_div.get_attribute("href")

            if image_url:
                regex = re.search(r"&iai=(.*)", image_url)
                if regex:
                    image_url = regex.group(1)
                    image_urls_array.append(image_url)
        return image_urls_array

    def get_search_titles(self):
        list_elements = self.driver.find_elements(*self.list_elements)
        search_titles = [title.text for title in list_elements]
        return search_titles
