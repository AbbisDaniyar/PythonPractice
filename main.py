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
        wait = WebDriverWait(driver, 10)
        # Считываем Exel
        # Находим и кликаем по ссылке для скачивания Excel
        download_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download Excel')]"))
        )
        download_link.click()

        # Даем время для скачивания файла
        time.sleep(3)

        excel_url = "Users\Daniyar\Download\schallenge.xlsx"
        df = pd.read_excel(excel_url)
        #Нажимаем на Кнопку старт
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))).click()
        #Заполняем все формы
        for index, row in df.iterrows():
            # Заполняем поля
            fields = ['labelFirstName', 'labelLastName', 'labelCompanyName',
                      'labelRole', 'labelAddress', 'labelEmail', 'labelPhone']

            values = [str(row['First Name']), str(row['Last Name ']), str(row['Company Name']),
                      str(row['Role in Company']), str(row['Address']), str(row['Email']),
                      str(row['Phone Number'])]

            for field, value in zip(fields, values):
                input_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"input[formcontrolname='{field}']")))
                input_field.clear()
                input_field.send_keys(value)

            # Отправляем форму
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Submit']"))).click()
            time.sleep(0.2)

        #Скриншот результата
        time.sleep(3)
        driver.save_screenshot("result.png")
        print("Скриншот сохранен!")



    except Exception as e:
        print(f"Ошибка: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    simple_solution()