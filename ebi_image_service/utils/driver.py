from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebDriver:
    DOWNLOAD_DIR = '/tmp'

    def __init__(self, headless=True):
        self.options = webdriver.ChromeOptions()

        self.options.add_argument('--disable-extensions')
        if headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')

        self.options.add_experimental_option(
            'prefs', {
                'download.default_directory': self.DOWNLOAD_DIR,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
        )

        self.driver = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)

    def close(self):
        self.driver.quit()

    def get(self, url):
        try:
            print("waiting...")
            self.driver.get(url)
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "RENDER_COMPLETE")))
            print("done")
        except Exception as e:
            print(e)
        finally:
            print("close")
            self.driver.close()
