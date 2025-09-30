import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def simple_solution():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Переходим на сайт
        driver.get("https://www.rpachallenge.com/")


    except Exception as e:
        print(f"Ошибка: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    simple_solution()