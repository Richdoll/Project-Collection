"""Selenium driver factory (headless Chrome), works locally and on Streamlit Cloud."""
import os
import shutil


def get_driver(headless: bool = True):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    for arg in ("--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--window-size=1366,900"):
        opts.add_argument(arg)
    opts.page_load_strategy = "eager"
    # Images are not loaded: faster scraping
    opts.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    for path in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"):
        if os.path.exists(path):
            opts.binary_location = path
            break

    driver_path = shutil.which("chromedriver") or next(
        (p for p in ("/usr/bin/chromedriver", "/usr/lib/chromium/chromedriver") if os.path.exists(p)), None
    )
    service = Service(driver_path) if driver_path else Service()  # otherwise Selenium Manager
    return webdriver.Chrome(service=service, options=opts)
