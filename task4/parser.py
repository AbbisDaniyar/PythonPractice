import os
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class DomkorParser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.setup_driver()
        self.all_apartments = {}

    def setup_driver(self):
        """Настройка драйвера Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def close_popup(self):
        """Закрытие всплывающего окна"""
        try:
            close_btn = self.driver.find_element(By.XPATH, "//a[@class='white-saas-generator-close-button']")
            close_btn.click()
            time.sleep(1)
        except:
            pass

    def get_jk_links(self):
        """Получение всех ссылок на ЖК с главной страницы"""
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            self.close_popup()

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            jk_links = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/prodazha-kvartir-Novostroiki/']")

            for element in elements:
                try:
                    href = element.get_attribute('href')
                    text = element.text.strip()

                    if (href and text and len(text) > 3 and
                            not any(
                                city in text for city in ["Набережные Челны", "Альметьевск", "Елабуга", "Нижнекамск"])):

                        lines = text.split('\n')
                        clean_title = lines[0].strip() if lines else text

                        if clean_title.lower() not in ['новостройки', 'акции', 'ипотека', 'паркинги', 'офисы']:
                            jk_info = {'title': clean_title, 'url': href}
                            if not any(jk['url'] == href for jk in jk_links):
                                jk_links.append(jk_info)
                except:
                    continue

            return jk_links

        except Exception as e:
            print(f"Ошибка при получении списка ЖК: {e}")
            return []

    def parse_apartment_data(self, html: str):
        """Парсинг данных квартиры из HTML"""
        try:
            pattern_common = r"<br>\s*([^<\s\n][^<\n]*?)\s*(?=<br>|$)"
            pattern_price = r"<font[^>]*>(.*?)</font>"
            pattern_no = r"№\s*(\d+)"

            results_common = re.findall(pattern_common, html)
            results_price = re.findall(pattern_price, html)
            results_no = re.findall(pattern_no, html)

            if not all([results_common, results_price, results_no]):
                return None

            rooms = re.sub(r"\D", "", results_common[0])
            apartment_no = results_no[0]
            price = results_price[1] if len(results_price) > 1 else results_price[0]
            area = results_common[2]

            try:
                rooms = int(rooms) if rooms else 1
            except:
                rooms = 1

            try:
                apartment_no = int(apartment_no)
            except:
                apartment_no = 101

            area_clean = re.sub(r'[^\d,.]', '', area).replace(',', '.')
            try:
                area_value = float(area_clean)
            except:
                area_value = 50.0

            price_clean = re.sub(r'[^\d,]', '', price).replace(',', '.')
            try:
                price_value = float(price_clean)
            except:
                price_value = area_value * 110000

            entrance = 1
            floor = (apartment_no % 100) // 10 if apartment_no > 100 else 1

            return {
                '№ Подъезда': entrance,
                'Этаж': floor,
                '№ Кв.': apartment_no,
                'Комнаты': rooms,
                'Общая площадь': area_value,
                'Цена': price_value,
                'Площадь строка': area,
                'Цена строка': price
            }

        except Exception as e:
            return None

    def parse_residential_complex(self, complex_url: str, jk_title: str):
        """Парсинг всего жилого комплекса"""
        try:
            self.driver.get(complex_url)
            time.sleep(3)
            self.close_popup()

            apartments = []

            try:
                divs = self.driver.find_elements(By.XPATH,
                                                 "//div[contains(@id, 'kvartira')]/following-sibling::div[@class='sh']")

                for div in divs:
                    try:
                        apartment_html = div.get_attribute("innerHTML")
                        apartment_data = self.parse_apartment_data(apartment_html)
                        if apartment_data:
                            apartments.append(apartment_data)
                    except:
                        continue
            except:
                pass

            return apartments

        except Exception as e:
            return []

    def run(self):
        """Основной метод запуска парсера"""
        try:
            print("Запуск парсера Domkor...")
            print(f"Базовая страница: {self.base_url}")

            jk_links = self.get_jk_links()

            if not jk_links:
                print("ЖК не найдены")
                return

            print(f"Найдено ЖК: {len(jk_links)}")

            for i, jk in enumerate(jk_links, 1):
                print(f"Обрабатываем {i}/{len(jk_links)}: {jk['title']}")

                apartments = self.parse_residential_complex(jk['url'], jk['title'])
                if apartments:
                    self.all_apartments[jk['title']] = apartments
                    print(f"Квартир: {len(apartments)}")
                else:
                    print(f"Не удалось получить данные")

                if i < len(jk_links):
                    time.sleep(1)

        except Exception as e:
            print(f"Критическая ошибка: {e}")

        finally:
            print("Завершение работы...")
            self.driver.quit()


def main():
    BASE_URL = "https://www.domkor-dom.com/prodazha-kvartir-Novostroiki/kvartira-Naberezhnye-Chelny/"
    parser = DomkorParser(BASE_URL)
    parser.run()


if __name__ == "__main__":
    main()