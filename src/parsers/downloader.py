import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


def download_plan(program_url: str, output_dir: str) -> str:
    """
    1) Открывает страницу в headless Chromium.
    2) Раскрывает окно и скроллит к кнопке.
    3) Кликает с помощью JS/ActionChains, повторяя при перехвате.
    4) Ждёт появления PDF в output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Пути к бинарникам (см. предыдущие исправления)
    chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    driver_bin = os.getenv("CHROME_DRIVER", "/usr/bin/chromedriver")

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    prefs = {
        "download.default_directory": os.path.abspath(output_dir),
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=driver_bin)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(program_url)

        # 1. Максимизируем окно, чтобы убрать побочные перекрытия  [oai_citation:7‡Stack Overflow](https://stackoverflow.com/questions/68072780/elementclickinterceptedexception-solutions-in-selenium-and-python?utm_source=chatgpt.com)
        driver.maximize_window()

        wait = WebDriverWait(driver, 15)
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Скачать учебный план')]")
        ))

        # 2. Скроллим к центру элемента  [oai_citation:8‡testrigor.com](https://testrigor.com/blog/elementclickinterceptedexception/?utm_source=chatgpt.com)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(0.5)  # ждём завершения анимации

        # 3. Пробуем клик и повторяем при перехвате  [oai_citation:9‡BrowserStack](https://www.browserstack.com/guide/element-click-intercepted-exception-selenium?utm_source=chatgpt.com) [oai_citation:10‡TestingBot](https://testingbot.com/resources/articles/selenium-elementclickinterceptedexception?utm_source=chatgpt.com)
        for attempt in range(3):
            try:
                btn.click()
                break
            except ElementClickInterceptedException:
                # Делаем клик через ActionChains как резервный вариант  [oai_citation:11‡GeeksforGeeks](https://www.geeksforgeeks.org/move_to_element-method-action-chains-in-selenium-python/?utm_source=chatgpt.com)
                ActionChains(driver).move_to_element(btn).click(btn).perform()
                time.sleep(0.5)
        else:
            raise RuntimeError("Не удалось кликнуть по кнопке загрузки после 3 попыток")

        # 4. Ожидаем файл в каталоге
        deadline = time.time() + 20
        while time.time() < deadline:
            pdfs = [f for f in os.listdir(output_dir) if f.lower().endswith(".pdf")]
            if pdfs:
                return os.path.join(output_dir, pdfs[0])
            time.sleep(0.5)

        raise RuntimeError("PDF не появился в output_dir за 20 секунд")
    finally:
        driver.quit()
