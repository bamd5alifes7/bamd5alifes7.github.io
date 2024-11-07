from contextlib import contextmanager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@contextmanager
def make_chrome_driver() -> Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = Chrome(service= service,
                    options= options)
    yield driver
    driver.quit()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

def test_button():

    #開啟網頁找到follow_me按鈕，點下去開啟新分頁，確定新分頁的網址如預期
    with make_chrome_driver() as driver:
        driver.get("https://bamd5alifes7.github.io/")
        sleep(2)

        button = WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.XPATH, "//a[@id='card-info-btn']")))

        #print("\n")
        #print(button.text)

        button.click()
        sleep(2)

        # 獲取所有分頁的 handle
        all_tabs = driver.window_handles
        # 切換到最新的分頁
        driver.switch_to.window(all_tabs[-1])

        # 取得當前 URL 並進行斷言
        follow_me_url = "https://github.com/bamd5alifes7"

        current_url = driver.current_url

        assert current_url == follow_me_url
