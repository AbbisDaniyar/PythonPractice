import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def rpa_challenge_solution():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        print("Загружаем сайт...")
        driver.get("https://www.rpachallenge.com/")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("Загружаем данные из Excel...")
        df = pd.read_excel("https://www.rpachallenge.com/assets/downloadFiles/challenge.xlsx")
        print(f"Найдено {len(df)} записей")

        print("Нажимаем кнопку Start...")
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
        )
        start_button.click()

        time.sleep(3)

        successful_forms = 0

        for i in range(len(df)):
            row = df.iloc[i]
            print(f"Обрабатываем запись {i + 1}/{len(df)}")

            field_data = {
                'labelFirstName': str(row['First Name']),
                'labelLastName': str(row['Last Name ']),
                'labelCompanyName': str(row['Company Name']),
                'labelRole': str(row['Role in Company']),
                'labelAddress': str(row['Address']),
                'labelEmail': str(row['Email']),
                'labelPhone': str(row['Phone Number'])
            }

            for field_name, value in field_data.items():
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"input[formcontrolname='{field_name}']"))
                )
                element.clear()
                element.send_keys(value)

            submit_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Submit']"))
            )
            submit_btn.click()
            successful_forms += 1

            time.sleep(0.5)

        print(f"Задание завершено! Успешно отправлено {successful_forms}/{len(df)} форм")

        time.sleep(3)
        driver.save_screenshot("result.png")
        print("Скриншот сохранен")

        result_element = driver.find_element(By.CLASS_NAME, "congratulations")
        print(result_element.text)

    except Exception as e:
        print(f"Ошибка: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    rpa_challenge_solution()