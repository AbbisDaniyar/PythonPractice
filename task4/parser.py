
import time
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