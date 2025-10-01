import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def working_solution():
    # Настройка Chrome options для обхода возможных блокировок
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    try:
        print("Загружаем сайт...")
        driver.get("https://www.rpachallenge.com/")

        # Ждем полной загрузки страницы
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Сайт загружен")

        # Читаем данные ДО нажатия кнопки Start
        print("Загружаем данные из Excel...")
        df = pd.read_excel("https://www.rpachallenge.com/assets/downloadFiles/challenge.xlsx")
        print(f"Найдено {len(df)} записей")

        # Нажимаем кнопку Start
        print("🔍 Ищем кнопку Start...")
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
        )
        print("Кнопка Start найдена")

        start_button.click()
        print("Челлендж начат!")

        # Пробуем разные селекторы для поиска формы
        form_selectors = [
            "input[formcontrolname]",  # Основной селектор
            "form input",  # Любой input в форме
            ".form-group input",  # Input в группе формы
            "input[ng-reflect-name]",  # Angular атрибут
            "input"  # Просто любой input
        ]

        form_found = False
        for selector in form_selectors:
            try:
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                if elements:
                    print(f"Форма найдена с селектором: {selector}")
                    print(f"Найдено {len(elements)} полей")
                    form_found = True
                    break
            except:
                continue

        if not form_found:
            print("Форма не загрузилась. Сохраняем скриншот для отладки...")
            driver.save_screenshot("debug_no_form.png")
            print("Скриншот сохранен как debug_no_form.png")

            # Пробуем продолжить в любом случае
            print("Пробуем продолжить...")
            elements = driver.find_elements(By.TAG_NAME, "input")
            print(f"Найдено {len(elements)} input элементов")

        # Заполняем формы
        successful_forms = 0

        for i in range(len(df)):
            row = df.iloc[i]
            print(f"\nОбрабатываем запись {i + 1}/{len(df)}")

            try:
                # Данные для текущей строки
                field_data = {
                    'labelFirstName': str(row['First Name']),
                    'labelLastName': str(row['Last Name ']),
                    'labelCompanyName': str(row['Company Name']),
                    'labelRole': str(row['Role in Company']),
                    'labelAddress': str(row['Address']),
                    'labelEmail': str(row['Email']),
                    'labelPhone': str(row['Phone Number'])
                }

                # Заполняем каждое поле
                for field_name, value in field_data.items():
                    try:
                        # Ищем поле разными способами
                        selectors = [
                            f"input[formcontrolname='{field_name}']",
                            f"input[ng-reflect-name='{field_name}']",
                            f"input[placeholder*='{field_name.replace('label', '')}']"
                        ]

                        element = None
                        for selector in selectors:
                            try:
                                element = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                )
                                break
                            except:
                                continue

                        if element:
                            element.clear()
                            element.send_keys(value)
                            print(f"   {field_name}: {value}")
                        else:
                            print(f"   Поле {field_name} не найдено")

                    except Exception as e:
                        print(f"    Ошибка в поле {field_name}: {e}")

                # Отправляем форму
                print("   Отправляем форму...")
                submit_selectors = [
                    "input[value='Submit']",
                    "button[type='submit']",
                    ".btn-primary",
                    "input[type='submit']"
                ]

                submit_found = False
                for selector in submit_selectors:
                    try:
                        submit_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        submit_btn.click()
                        submit_found = True
                        print("   Форма отправлена")
                        successful_forms += 1
                        break
                    except:
                        continue

                if not submit_found:
                    print("   Кнопка Submit не найдена")

                # Ждем перед следующей формой
                time.sleep(1)

            except Exception as e:
                print(f" Ошибка при обработке записи {i + 1}: {e}")
                continue

        # Финальный результат
        print(f"\n Задание завершено! Успешно отправлено {successful_forms}/{len(df)} форм")

        # Сохраняем скриншот
        time.sleep(3)
        driver.save_screenshot("final_result.png")
        print(" Скриншот сохранен как final_result.png")

        # Пытаемся получить текст результата
        try:
            result_elements = driver.find_elements(By.CLASS_NAME, "congratulations")
            if result_elements:
                print(f"Результат: {result_elements[0].text}")
        except:
            print("ℹТекст результата не найден")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        driver.save_screenshot("error.png")
        print("Скриншот ошибки сохранен")
    finally:
        print("Завершаем работу")
        driver.quit()


if __name__ == "__main__":
    working_solution()