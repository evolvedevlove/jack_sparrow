import unittest
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def launch_browser(url):
    """ launch and return a browser  """
    chromedriver_service = Service('../chromedriver.exe')
    new_browser_driver = wd.Chrome(service=chromedriver_service)
    new_browser_driver.get(url)
    new_browser_driver.set_window_rect(x=930, y=0, width=1100, height=1125)
    return new_browser_driver


def wait_for_browser_ready(browser, condition):
    """ called from within functions outside of main """
    # wait until the page is loaded
    waiter = WebDriverWait(browser, 100)
    ready = waiter.until(EC.element_to_be_clickable((By.ID, condition)))
    return ready


class SearchTest(unittest.TestCase):
    def setUp(self):
        """ set up for individual test run - could be structured to run a suite a tests instead of one at a time"""
        url = "https://codility-frontend-prod.s3.amazonaws.com/media/task_static/qa_csharp_search/862b0faa506b8487c25a3384cfde8af4/static/attachments/reference_page.html"
        self.driver = launch_browser(url)

    def test_input_query_id(self):
        """ query input has id equal to search-input """
        wait_for_browser_ready(self.driver, "search-button")
        input_query_id_element = self.driver.find_element(By.ID, 'search-input')
        input_query_id_value = input_query_id_element.get_attribute("id")

        # expected value, actual value
        self.assertEqual('search-input', input_query_id_value)

    def test_input_button_id(self):
        """ query input has id equal to search-button """
        wait_for_browser_ready(self.driver, "search-button")
        input_button_id_element = self.driver.find_element(By.ID, 'search-button')
        input_query_id_value = input_button_id_element.get_attribute("id")

        # expected value, actual value
        self.assertEqual('search-button', input_query_id_value)

    def test_empty_query(self):
        """ empty query is forbidden """
        wait_for_browser_ready(self.driver, "search-button")
        self.driver.find_element(By.ID, "search-button").click()
        wait_for_browser_ready(self.driver, "search-button")

        error_empty_query_id_exp = "error-empty-query"
        error_empty_query_div_element = self.driver.find_element(By.ID, error_empty_query_id_exp)

        # expected value, actual value
        self.assertEqual(error_empty_query_id_exp, error_empty_query_div_element.get_attribute("id"))

    def test_more_than_one_result(self):
        """ at least one result is returned """
        wait_for_browser_ready(self.driver, "search-button")
        self.driver.find_element(By.ID, 'search-input').send_keys("isla")
        self.driver.find_element(By.ID, 'search-button').click()
        wait_for_browser_ready(self.driver, "search-results")

        page_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        ul = page_soup.find(id='search-results')
        list_items = list(ul.children)

        # expected value, actual value
        self.assertLess(0, len(list_items))

    def test_no_results(self):
        """ no valid results to return """
        wait_for_browser_ready(self.driver, "search-button")
        self.driver.find_element(By.ID, 'search-input').send_keys("castle")
        self.driver.find_element(By.ID, 'search-button').click()
        wait_for_browser_ready(self.driver, "search-results")

        page_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        error_no_results_div = page_soup.find(id='error-no-results')
        error_no_results_div_text = error_no_results_div.text

        # expected value, actual value
        self.assertEqual("No results", error_no_results_div_text)

    def test_query_match(self):
        """ single record is returned from query """
        self.driver.find_element(By.ID, "search-input").send_keys("Port Royal")
        self.driver.find_element(By.ID, 'search-button').click()
        wait_for_browser_ready(self.driver, "search-results")

        page_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        ul_results = page_soup.find(id='search-results')
        search_results_text = ul_results.text

        # expected value, actual value
        self.assertEqual("Port Royal", search_results_text)

    def tearDown(self):
        """ ran after each test """
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
