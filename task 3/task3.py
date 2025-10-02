"""
Color Game Bot - автоматизация игры на определение цветов
https://www.arealme.com/colors/ru/
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from collections import Counter


class ColorGameBot:
    """Основной класс бота для цветовой игры"""

    def __init__(self):
        self.setup_driver()
        self.score = 0

    def setup_driver(self):
        """Настройка Chrome драйвера"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_window_size(1200, 800)

    def start_game(self):
        """Запуск игры"""
        print(" Запуск бота...")
        self.driver.get("https://www.arealme.com/colors/ru/")
        time.sleep(2)

        start_btn = self.driver.find_element(By.ID, "start")
        start_btn.click()
        print("🎮 Игра начата!")
        time.sleep(2)

    def find_color_elements(self):
        """Поиск цветных элементов на странице"""
        try:
            container = self.driver.find_element(By.CSS_SELECTOR, ".patra-color")
            spans = container.find_elements(By.TAG_NAME, "span")

            color_elements = []
            for span in spans:
                try:
                    bg_color = span.value_of_css_property('background-color')
                    if bg_color and bg_color.startswith('rgb'):
                        color_elements.append(span)
                except:
                    continue

            return color_elements
        except:
            return []

    def find_unique_color(self, elements):
        """Поиск уникального цвета среди элементов"""
        if len(elements) < 4:
            return None

        colors = []
        for element in elements:
            try:
                color = element.value_of_css_property('background-color')
                colors.append(color)
            except:
                continue

        color_count = Counter(colors)
        for color, count in color_count.items():
            if count == 1:
                for element in elements:
                    if element.value_of_css_property('background-color') == color:
                        return element

        return None

    def play_round(self):
        """Выполнение одного раунда игры"""
        elements = self.find_color_elements()
        if not elements:
            return False

        unique_element = self.find_unique_color(elements)
        if unique_element:
            try:
                unique_element.click()
                self.score += 1
                return True
            except:
                return False

        return False

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()


def main():
    bot = ColorGameBot()
    try:
        bot.start_game()

        # Простая демонстрация
        for i in range(10):
            if bot.play_round():
                print(f"Успешный клик! Счет: {bot.score}")
            time.sleep(1)

        print(f"Финальный счет: {bot.score}")

    finally:
        bot.close()


if __name__ == "__main__":
    main()