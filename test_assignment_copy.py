from selenium import webdriver
from pages.duck_duck_go_page import SearchResultsPage
import re
import pytest
import utils.baseUrl as baseUrl


# Defining pytest fixture which returns an instance of driver
@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


# 1. navigating across browser starts here
def test_search_duck_duck_go(driver):
    # Creates an instance of the SearchResultsPage class
    search_results_page = SearchResultsPage(driver)

    # opens url
    search_results_page.open_url(baseUrl.base_url)

    # takes in string parameter and searches
    search_results_page.perform_search("cartoons wallpapercave")

    # error handling for when images are not present
    search_results_page.confirm_images_present()

    # collects and prints image urls
    image_urls = search_results_page.get_image_urls()
    print(image_urls)

    # collects and prints titles avoiding adds
    search_titles = search_results_page.get_search_titles()
    print(search_titles)

    # test that passes if at least one url comes from wallpaper
    assert any("wallpapercave.com" in image_url for image_url in image_urls)

    #  test that passes if at least one title has word Car in it
    assert any(
        re.search(r"\bCar(s)?\b", title, re.IGNORECASE) for title in search_titles
    )


if __name__ == "__main__":
    pytest.main()
