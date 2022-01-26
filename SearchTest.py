import unittest
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def launch_browser(url):
    """ launch and return a browser  """
    chromedriver_service = Service('./chromedriver.exe')
    new_browser_driver = wd.Chrome(service=chromedriver_service)
    new_browser_driver.get(url)
    new_browser_driver.set_window_rect(x=930, y=0, width=1100, height=1125)
    return new_browser_driver

def wait_for_browser_ready(browser, condition):
    """ called from within functions outside of main """
    # wait until the page is loaded
    waiter = WebDriverWait(browser, 10)
    ready = waiter.until(EC.element_to_be_clickable((By.ID, condition)))
    return ready



def main():
    url = "https://codility-frontend-prod.s3.amazonaws.com/media/task_static/qa_csharp_search/862b0faa506b8487c25a3384cfde8af4/static/attachments/reference_page.html"
    driver = launch_browser(url)


if __name__ == '__main__':
    main()